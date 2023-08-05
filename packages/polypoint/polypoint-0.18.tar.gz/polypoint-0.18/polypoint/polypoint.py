import multiprocessing as mp
from multiprocessing import Manager, Pool as ThreadPool
import numpy as np

import pyximport; pyximport.install()
from .utils import point_in_polygon, xml_parse, get_polygon_extremities, segments, get_area, cross_sign, trim_polygons

from .config import Configuration

class PolygonClassifier:
    def __init__(self):
        self.conf = None
        self.test_point_member_list = []

    def initialize_min(self, polygon_file_name="states.xml", search_update_freq=5000):
        self.conf = Configuration()
        self.conf.name_list, self.conf.polygon_list = xml_parse(polygon_file_name)
        self.conf.search_order = [i for i in range(len(self.conf.polygon_list))]
        self.conf.frequency_dict = {x: 0 for x in range(len(self.conf.polygon_list))}
        self.conf.total_searched = 0
        self.conf.search_update_freq = search_update_freq

    def initialize(self, polygon_file_name="states.xml", parallel_enabled=True, num_cpu=0, parallel_limit=0, minimum_coverage=0.0, minimum_num_points=3, search_update_freq=5000):
        self.conf = Configuration()
        self.conf.parallel_enabled = parallel_enabled
        if num_cpu == 0:
            self.conf.num_cpu = mp.cpu_count()
        else:
            self.conf.num_cpu = num_cpu
        self.conf.parallel_limit = parallel_limit
        self.conf.minimum_coverage = minimum_coverage
        self.conf.minimum_num_points = minimum_num_points
        
        self.conf.name_list, self.conf.polygon_list = xml_parse(polygon_file_name)
        self.conf.polygon_extremities = get_polygon_extremities(self.conf.polygon_list)
        self.conf.trimmed_polygons = trim_polygons(self.conf, self.conf.polygon_list)
        self.conf.search_order = [i for i in range(len(self.conf.polygon_list))]
        self.conf.frequency_dict = {x: 0 for x in range(len(self.conf.polygon_list))}
        self.conf.total_searched = 0
        self.conf.search_update_freq = search_update_freq

    def _update_search_order(self):
        combined = [(i, self.conf.frequency_dict[i]) for i in self.conf.search_order]
        sorted_combined = sorted(combined, key= lambda x: x[1], reverse=True)
        self.conf.search_order = [x[0] for x in sorted_combined]
        self.conf.frequency_dict = {x: 0 for x in range(len(self.conf.polygon_list))}
        self.conf.total_searched = 0

    def _get_polygon_name(self, i):
        if i == -1:
            return "UNKNOWN"
        else:
            return self.conf.name_list[i]

    def get_polygon_names(self, point_list):
        """
        Returns the polygon names for a list of results.
        """
        polygon_names = []
        for e in point_list:
            polygon_names.append(self._get_polygon_name(e))
        return polygon_names

    def _point_in_polygon_opt(self, test_point, i):
        """
        Determine whether or not a point is in a polygon given a test point and a
        set of points describing a polygon. First checks if point is outside a 
        circumscribed square, then checks if point is inside a trimmed, interior
        polygon, and finally, if necessary, checks if point is inside the polygon.
        """
        # if the point is outside a bounding box for the polygon, it cannot possibly 
        # be inside the polygon, return false
        ext = self.conf.polygon_extremities[i]
        if test_point[0] > ext[0] or test_point[1] < ext[1] or test_point[0] < ext[2] or test_point[1] > ext[3]:
            return False

        # if the point is inside the trimmed interior polygon, return true
        if point_in_polygon(test_point[0], test_point[1], self.conf.trimmed_polygons[i]):
            return True

        # finally, check if the point is in the polygon directly
        return point_in_polygon(test_point[0], test_point[1], self.conf.polygon_list[i])

    def _get_containing_polygon(self, test_point):
        """
        Given a test point, this checks whether or not a test point is a member of
        any polygons in a given set. Note that this will return an invalid index 
        upon failing to find a polygon. 
        """
        polygon_member = -1
        for i in self.conf.search_order:
            if (point_in_polygon(test_point[0], test_point[1], self.conf.polygon_list[i])):
                polygon_member = i
                self.conf.frequency_dict[i] += 1
                break
        self.conf.total_searched += 1
        if self.conf.total_searched % self.conf.search_update_freq == 0:
            self._update_search_order()
        return polygon_member

    def _get_containing_polygon_opt(self, test_point):
        """
        Given a test point, this checks whether or not a test point is a member of
        any polygons in a given set. Note that this will return an invalid index 
        upon failing to find a polygon. 
        """
        polygon_member = -1
        for i in self.conf.search_order:
            if (self._point_in_polygon_opt(test_point, i)):
                polygon_member = i
                self.conf.frequency_dict[i] += 1
                break
        self.conf.total_searched += 1
        if self.conf.total_searched % self.conf.search_update_freq == 0:
            self._update_search_order()
        return polygon_member

    def _set_results(self, test_point_member_list_and_index):
        """
        Callback method for each worker in the pool.
        Assigns results to single class variable.
        """
        test_point_list = test_point_member_list_and_index[0]
        beg_ind = test_point_member_list_and_index[1]
        for i, e in enumerate(test_point_list):
            self.test_point_member_list[i + beg_ind] = e

    def _match_sublist_to_polygon(self, test_point_list, beg_ind):
        """
        Routine for workers in pool.
        Finds polygon (if any) that contains each point in the list.
        """
        test_point_list_matches = np.empty([len(test_point_list)], dtype=int)
        for i, e in enumerate(test_point_list):
            test_point_list_matches[i] = self._get_containing_polygon_opt(e)
        return test_point_list_matches, beg_ind

    def match_points_to_polygon(self, test_point_list):
        """
        Given a list of points, distributes calculations among a pool of workers.
        If parallelism is disabled, computes them sequentially.
        """
        length = len(test_point_list)
        self.test_point_member_list = np.empty([length], dtype=int)

        if(self.conf.parallel_enabled and self.conf.num_cpu > 1 and length > self.conf.parallel_limit
                and self.conf.polygon_extremities != None and self.conf.trimmed_polygons != None):
            pool = ThreadPool(self.conf.num_cpu)
            chunk_size = length / self.conf.num_cpu
            for i in range(self.conf.num_cpu):
                beg_ind = int((chunk_size) * i)
                end_ind = int((chunk_size) * (i + 1))
                if(i == self.conf.num_cpu - 1):
                    end_ind = length
                pool.apply_async(self._match_sublist_to_polygon, args=(
                    test_point_list[beg_ind:end_ind], beg_ind), callback=self._set_results)
            pool.close()
            pool.join()
        else:
            for i, test_point in enumerate(test_point_list):
                self.test_point_member_list[i] = self._get_containing_polygon(test_point)
        return self.test_point_member_list
