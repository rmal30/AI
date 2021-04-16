import heapq

class PriorityQueue:
    def __init__(self):
        self.items = []

    def put(self, item, priority):
        heapq.heappush(self.items, (priority, item))

    def pop(self):
        return heapq.heappop(self.items)
