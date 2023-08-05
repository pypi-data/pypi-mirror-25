class Configuration:
    def __init__(self):
        # list of polygon names and corresponding points
        self.name_list, self.polygon_list = None, None
        # enable parallel computation
        self.parallel_enabled = None
        # global variable for results so that processes can operate on same object
        self.test_point_member_list = None
        # leave as 0 to use one process per core, assign to change number of threads
        self.num_cpu = None
        # minimum number of points needed to enable parallel computation
        self.parallel_limit = None
        # list containing tuple for each polygon containing the highest, lowest,
        # leftmost, and rightmost points
        self.polygon_extremities = None
        # minimum coverage of each polygon
        self.minimum_coverage = None
        # least amount of points that a trimmed polygon may have
        self.minimum_num_points = None
        # trim polygons
        self.trimmed_polygons = None
        self.search_order = None
        self.frequency_dict = None
        self.total_searched = None
        self.search_update_freq = None
