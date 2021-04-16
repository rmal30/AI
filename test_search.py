import sys
import importlib
import datetime
from algo.search import Search

method_name = sys.argv[1]
search_query_name = sys.argv[2]

puzzle = importlib.import_module("search_queries." + search_query_name)

solver = Search(puzzle.query)
method = getattr(solver, method_name)

start_time = datetime.datetime.now()
sol = method()
end_time = datetime.datetime.now()

print(sol)
print(len(sol) - 1)
print(end_time - start_time)