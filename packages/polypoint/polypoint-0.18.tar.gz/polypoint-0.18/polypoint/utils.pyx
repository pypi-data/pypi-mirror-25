import os
import xml.etree.ElementTree
from pkg_resources import resource_filename
import numpy as np

cpdef int point_in_polygon(double lat, double lon, polygon):
    """
    Determine whether or not a point is in a polygon given a test point and a
    set of points describing a polygon.
    """
    cdef int polygon_len
    polygon_len = len(polygon)

    # start with the winding number equal to zero
    cdef int winding_number
    winding_number = 0
    
    # for each pair of points in the array, see if the line formed by those
    # two points crosses a horizontal line extending from the test point
    # to positive infinity. If it crosses upwards, add 1 to the winding number. 
    # If it crosses downwards, subtract 1 from the winding number. 
    cdef int j
    cdef double poly1_y, poly1_x, poly2_y, poly2_x
    cdef double dt
    for j in range(polygon_len):
        poly1_y, poly1_x = polygon[j]
        poly2_y, poly2_x = polygon[(j + 1) % polygon_len]
        if poly1_y <= lat:
            if poly2_y > lat:
                dt = ((poly2_x - poly1_x) * (lat - poly1_y) - (
                    lon - poly1_x) * (poly2_y - poly1_y))
                if dt > 0:
                    winding_number += 1
        else:
            if poly2_y <= lat:
                dt = ((poly2_x - poly1_x) * (lat - poly1_y) - (
                    lon - poly1_x) * (poly2_y - poly1_y))
                if dt < 0:
                    winding_number -= 1

    # if the winding number is not 0, the point is in the polygon
    return winding_number != 0

cpdef xml_parse(polygon_file_name):
    xml_file_name = os.path.abspath(resource_filename('polypoint', polygon_file_name))
    root = xml.etree.ElementTree.parse(xml_file_name).getroot()
    name_list = []
    point_lists = []

    for polygon in root:
        point_list = []
        for point in polygon:
            point_list.append(
                (float(point.attrib['lat']), float(point.attrib['lng'])))
        name_list.append(polygon.attrib['name'])
        if point_list[0] == point_list[-1]:
            point_list = point_list[:-1]
        point_lists.append(point_list)
    return name_list, np.array(point_lists)

cpdef get_polygon_extremities(polygon_list):
    polygon_extremities = []
    for array in polygon_list:
        t = [array[0][0], array[0][1], array[0][0], array[0][1]]
        for point in array:
            if point[0] > t[0]:
                t[0] = point[0]
            elif point[0] < t[2]:
                t[2] = point[0]
            if point[1] < t[1]:
                t[1] = point[1]
            elif point[1] > t[3]:
                t[3] = point[1]
        polygon_extremities.append(t)
    return polygon_extremities

cpdef segments(p):
    return zip(p, p[1:] + [p[0]])

def get_area(p):
    return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in segments(p)))

cpdef double cross_sign(x1, y1, x2, y2):
    return x1 * y2 > x2 * y1

cpdef double area_expected_runtime(int num_points_left, double original_polygon_length, double point_area, double polygon_area, double original_polygon_area):
    """
    The runtime is roughly equal to the number of points used to check if a point is in a polygon:
    (points in trimmed polygon) + (chance the point is in the trimmed polygon)*(points in original polygon)
    """
    return num_points_left + ((original_polygon_area - (polygon_area - point_area))/original_polygon_area)*original_polygon_length

cpdef worth_it(double original_polygon_area, int original_polygon_length, polygon, double polygon_area, int min_index, double point_area):
    """
    Determines if point in a polygon is worth removing. Returns true/false depending on 
    if removing the point at the given index decreases the expected runtime of the search. 
    """
    # if there are less than four points left, removing a point would not result in a polygon
    cdef int num_points_left = len(polygon)
    if num_points_left < 4:
        return False

    # retrieve the given point and the points before and after it
    cdef double p1_0 = polygon[(min_index - 1) % num_points_left][0]
    cdef double p1_1 = polygon[(min_index - 1) % num_points_left][1]
    cdef double p2_0 = polygon[min_index][0]
    cdef double p2_1 = polygon[min_index][1]
    cdef double p3_0 = polygon[(min_index + 1) % num_points_left][0]
    cdef double p3_1 = polygon[(min_index + 1) % num_points_left][1]
    cdef double v1_0 = p2_1 - p1_1
    cdef double v1_1 = p2_0 - p1_0
    cdef double v2_0 = p3_1 - p2_1
    cdef double v2_1 = p3_0 - p2_0

    # compute the cross sign, if false (negative) return early
    if not cross_sign(v1_1, v1_0, v2_1, v2_0):
        return False

    # calculate the old expected runtime and the new expected runtime
    # compare the new runtime to the old and if it's improved, return True
    cdef double old_expected_runtime = area_expected_runtime(num_points_left, original_polygon_length, 0, polygon_area, original_polygon_area)
    cdef double new_expected_runtime = area_expected_runtime(num_points_left - 1, original_polygon_length, point_area, polygon_area, original_polygon_area)
    return new_expected_runtime < old_expected_runtime

def trim_polygon(conf, polygon):
    """
    Returns polygon contained by original polygon with a better area per point ratio.
    """
    # save some attributes about the original polygon and a copy to edit in the loop
    cdef double original_polygon_area = get_area(polygon)
    cdef int original_polygon_length = len(polygon)
    polygon_area = original_polygon_area

    # make a list of areas for each point in the polygon formed by the point and its two neighbors
    area_list = [get_area([polygon[(i - 1) % len(polygon)], polygon[i], polygon[(i + 1) % len(polygon)]]) for i,e in enumerate(polygon)]
    
    # trim the polygon while there are more points left than specified (see minimum_num_points default value) 
    # and while more area is covered than specified (see minimum_coverage default value)
    while len(polygon) > conf.minimum_num_points and (polygon_area > (conf.minimum_coverage * original_polygon_area)):
        # make a list of booleans for each point in the list: 
        # true if removing it will decrease runtime, false otherwise
        worth_it_list = [worth_it(original_polygon_area, original_polygon_length, polygon, polygon_area, i, area_list[i]) for i,e in enumerate(polygon)]
        
        # if any points should be removed, remove one. Else, break. 
        if True in worth_it_list:
            # zip worth_it_list, area_list, and their indices together
            zipped_worth_it_list = zip(worth_it_list, area_list, range(len(polygon)))

            # sort the zipped list based on their areas (smallest -> largest)
            # save the sorted list and its indices in separate lists
            zipped_worth_it_list = list(sorted(zipped_worth_it_list, key=lambda x: x[1]))
            sorted_worth_it_list = [x[0] for x in zipped_worth_it_list]
            sorted_index_list = [x[2] for x in zipped_worth_it_list]

            # get the index of the point that should be removed and has the least area
            # associated with it
            i = sorted_worth_it_list.index(True)

            # get the pre-sorted index
            worth_it_index = sorted_index_list[i]

            # save the deleted point in case it needs to be restored
            deleted_point = polygon[worth_it_index]

            # delete the polygon and its associated area
            del polygon[worth_it_index]
            del area_list[worth_it_index]

            # the neighboring points are incorrect, recalculate the areas
            area_list[worth_it_index % len(polygon)] = get_area([polygon[(worth_it_index - 1) % len(polygon)], polygon[worth_it_index % len(polygon)], polygon[(worth_it_index + 1) % len(polygon)]])
            area_list[(worth_it_index - 1) % len(polygon)] = get_area([polygon[(worth_it_index - 2) % len(polygon)], polygon[(worth_it_index - 1) % len(polygon)], polygon[(worth_it_index) % len(polygon)]])
            

            # recalculate the area of the polygon
            polygon_area = get_area(polygon)

            # if removing the point reduced the area by too much, restore it.
            # then, since the point with the least area was chosen, break the loop
            if polygon_area < (conf.minimum_coverage * original_polygon_area):
                polygon.insert(worth_it_index, deleted_point)
                break
        else:
            break
    return polygon

def is_polygon_counterclockwise(polygon):
    """
    Checks if the points in a polygon are listed in counterclockwise order
    """
    return sum((x2 - x1)*(y2 + y1) for ((x1, y1), (x2, y2)) in segments(polygon)) < 0

cpdef trim_polygons(conf, polygon_list):
    """
    Trims all polygons in array.
    """
    trimmed_polygons = []
    for polygon in polygon_list:
        if not is_polygon_counterclockwise(polygon):
            polygon.reverse()
        trimmed_polygons.append(trim_polygon(conf, polygon[:]))
    return trimmed_polygons
