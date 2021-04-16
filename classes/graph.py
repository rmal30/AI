class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.neighbours = {}

    def add_node(self, key, node):
        self.nodes[key] = node
        self.neighbours[key] = set()

    def add_edge(self, a, b, dist):
        self.edges[(a, b)] = dist
        self.edges[(b, a)] = dist
        self.neighbours[a].add(b)
        self.neighbours[b].add(a)

    def remove_edge(self, a, b):
        del self.edges[(a, b)]
        del self.edges[(b, a)]
        self.neighbours[a].remove(b)
        self.neighbours[b].remove(a)