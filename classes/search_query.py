class SearchQuery:
    def __init__(self, start_node, goal_node, get_neighbours = None, get_edges = None, heuristic_func = None):
        self.start_node = start_node
        self.goal_node = goal_node
        self.get_neighbours = get_neighbours
        self.get_edges = get_edges
        self.h = heuristic_func