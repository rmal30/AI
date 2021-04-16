import sys
import importlib
import datetime
from algo.constraint_solver import ConstraintSolver

method_name = sys.argv[1]
puzzle_name = sys.argv[2]

puzzle = importlib.import_module("csps." + puzzle_name)

solver = ConstraintSolver(puzzle.problem)
method = getattr(solver, method_name)

start_time = datetime.datetime.now()
sol = method()
end_time = datetime.datetime.now()

puzzle.show_solution(sol)
print(end_time - start_time)