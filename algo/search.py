from collections import deque
from utils import PriorityQueue

class Search:
    @staticmethod
    def get_path(start, goal, parents):
        path = []
        node = goal
        while node in parents and node != start:
            path.append(node)
            node = parents[node]
        path.append(node)
        path.reverse()
        return path

    def __init__(self, query):
        self.query = query

    def dfs(self):
        stack = []
        stack.append(self.query.start_node)
        visited = set([self.query.start_node])
        parents = {}
        while stack:
            node = stack.pop()
            for neighbour_node in self.query.get_neighbours(node):
                if neighbour_node == self.query.goal_node:
                    parents[neighbour_node] = node
                    return Search.get_path(self.query.start_node, self.query.goal_node, parents)
                elif neighbour_node not in visited:
                    visited.add(neighbour_node)
                    stack.append(neighbour_node)
                    parents[neighbour_node] = node
        return None

    @staticmethod
    def dls(start_node, goal_node, get_neighbours, depth):
        if start_node == goal_node:
            return []
        elif depth == 0:
            return None

        for neighbour_node in get_neighbours(start_node):
            found = Search.dls(neighbour_node, goal_node, get_neighbours, depth - 1)
            if found is not None:
                return [neighbour_node] + found
        return None

    def idfs(self):
        depth = 0
        found = None
        while found is None:
            depth += 1
            found = Search.dls(self.query.start_node, self.query.goal_node, self.query.get_neighbours, depth)
            print(depth)

        return found

    def bfs(self):
        queue = deque()
        queue.append(self.query.start_node)
        visited = set([self.query.start_node])
        parents = {}
        while queue:
            node = queue.popleft()
            for neighbour_node in self.query.get_neighbours(node):
                if neighbour_node == self.query.goal_node:
                    parents[neighbour_node] = node
                    return Search.get_path(self.query.start_node, self.query.goal_node, parents)
                elif neighbour_node not in visited:
                    parents[neighbour_node] = node
                    visited.add(neighbour_node)
                    queue.append(neighbour_node)
        return None

    def bidirectional_bfs(self):
        start_queue = deque()
        end_queue = deque()
        start_queue.append(self.query.start_node)
        end_queue.append(self.query.goal_node)
        start_visited = set([self.query.start_node])
        end_visited = set([self.query.goal_node])
        start_parents = {}
        end_parents = {}
        while not set.intersection(set(start_queue), set(end_queue)):
            node1 = start_queue.popleft()
            for neighbour_node1 in self.query.get_neighbours(node1):
                if neighbour_node1 not in start_visited:
                    start_visited.add(neighbour_node1)
                    start_queue.append(neighbour_node1)
                    start_parents[neighbour_node1] = node1

            node2 = end_queue.popleft()
            for neighbour_node2 in self.query.get_neighbours(node2):
                if neighbour_node2 not in end_visited:
                    end_visited.add(neighbour_node2)
                    end_queue.append(neighbour_node2)
                    end_parents[neighbour_node2] = node2

        center_node = set.intersection(set(start_queue), set(end_queue)).pop()
        start_path = Search.get_path(self.query.start_node, center_node, start_parents)
        end_path = Search.get_path(self.query.goal_node, center_node, end_parents)
        end_path.reverse()
        return start_path[:-1] + end_path

    def ucs(self):
        parents = {}
        queue = PriorityQueue()
        queue.put(self.query.start_node, 0)
        visited = set([self.query.start_node])
        while queue.items:
            (depth, node) = queue.pop()
            for edge, neighbour_node in self.query.get_edges(node):
                if neighbour_node == self.query.goal_node:
                    return Search.get_path(self.query.start_node, self.query.goal_node, parents)
                elif neighbour_node not in visited:
                    visited.add(neighbour_node)
                    queue.put(neighbour_node, depth + edge)
                    parents[neighbour_node] = node
        return None

    def a_star(self):
        parents = {}
        open_dists = PriorityQueue()
        open_dists.put(self.query.start_node, self.query.h(self.query.start_node))
        visited = set([self.query.start_node])
        g = {}
        g[self.query.start_node] = 0

        while open_dists.items:
            (_, node) = open_dists.pop()
            #print(node)
            for edge, neighbour_node in self.query.get_edges(node):
                if neighbour_node == self.query.goal_node:
                    parents[neighbour_node] = node
                    return Search.get_path(self.query.start_node, self.query.goal_node, parents)
                new_g = g[node] + edge
                if neighbour_node not in visited or new_g < g[neighbour_node]:
                    g[neighbour_node] = new_g
                    open_dists.put(neighbour_node, new_g + self.query.h(neighbour_node))
                    parents[neighbour_node] = node
                    visited.add(neighbour_node)
        return None

    def ida_star(self):
        thresh = self.query.h(self.query.start_node)
        while True:
            temp = Search.dfs_astar(self.query.start_node, self.query.goal_node, 0, thresh, self.query.get_edges, self.query.h)
            if type(temp) is list:
                return temp
            print(temp)
            thresh = temp

    @staticmethod
    def dfs_astar(node, goal_node, g, thresh, get_edges, h):
        f = g + h(node)
        if f > thresh:
            return f
        if node == goal_node:
            return [goal_node]

        min_thresh = -1
        for edge, neighbour_node in get_edges(node):
            path = Search.dfs_astar(neighbour_node, goal_node, g + edge, thresh, get_edges, h)
            if type(path) is list:
                return [node] + path
            if min_thresh == -1 or path < min_thresh:
                min_thresh = path
        return min_thresh

    def best_first(self):
        parents = {}
        open_dists = PriorityQueue()
        open_dists.put(self.query.start_node, self.query.h(self.query.start_node))
        visited = set([self.query.start_node])

        while open_dists.items:
            (_, node) = open_dists.pop()
            for neighbour_node in self.query.get_neighbours(node):
                if neighbour_node == self.query.goal_node:
                    return Search.get_path(self.query.start_node, self.query.goal_node, parents)
                if neighbour_node not in visited:
                    open_dists.put(neighbour_node, self.query.h(neighbour_node))
                    parents[neighbour_node] = node
                    visited.add(neighbour_node)
        return None