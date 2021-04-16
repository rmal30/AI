from classes.csp import CSP

N = 9

def row_constraint(vals):
    return len(vals) == len(set(vals))

def col_constraint(vals):
    return len(vals) == len(set(vals))

def box_constraint(vals):
    return len(vals) == len(set(vals))

def sudoku_heuristic(vals):
    return len(vals) - len(set(vals))
"""
init = {
    0:  1,  5: 7,  7: 9,
    10: 3, 13: 2, 17: 8,
    20: 9, 21: 6, 24: 5,
    29: 5, 30: 3, 33: 9,
    37: 1, 40: 8, 44: 2,
    45: 6, 50: 4,
    54: 3, 61: 1,
    64: 4, 71: 7,
    74: 7, 78: 3
}
"""

init = {
    0:  8,
    11: 3, 12: 6,
    19: 7, 22: 9, 24: 2,
    28: 5, 32: 7,
    40: 4, 41: 5, 42: 7,
    48: 1, 52: 3,
    56: 1, 61: 6, 62: 8,
    65: 8, 66: 5, 70: 1,
    73: 9, 78: 4
}

"""
init = {
    3: 7,
    9: 1,
    21: 4, 22: 3, 24: 2,
    35: 6,
    39: 5, 41: 9,
    51: 4, 52: 1, 53: 8,
    58: 8, 59: 1,
    65: 2, 70: 5,
    73: 4, 78: 3
}
"""
"""
init = {
    5: 5, 7: 8,
    12: 6, 14: 1, 16: 4, 17: 3,
    28: 1, 30: 5,
    39: 1, 41: 6,
    45: 3, 52: 5,
    54: 5, 55: 3, 61: 6, 62: 1,
    71: 4
}
"""

problem = CSP(init)
for i in range(N*N):
    if i in init:
        problem.add_variable(i, [init[i]])
    else:
        problem.add_variable(i, range(1, N + 1))

for i in range(N):
    problem.add_constraint(range(i*N, i*N + N), row_constraint)
    problem.add_constraint(range(i, i + N*(N - 1) + 1, N), col_constraint)
    problem.add_heuristic(range(i*N, i*N + N), sudoku_heuristic)
    problem.add_heuristic(range(i, i + N*(N - 1) + 1, N), sudoku_heuristic)

def gen_line(n):
    return (n*3, n*3 + 1, n*3 + 2)

x = {}
for i in range(27):
    x[i] = gen_line(i)
for i in (0, 1, 2, 9, 10, 11, 18, 19, 20):
    problem.add_constraint(x[i] + x[i+3] + x[i+6], box_constraint)
    problem.add_heuristic(x[i] + x[i+3] + x[i+6], sudoku_heuristic)

def show_solution(sol):
    if isinstance(sol, list):
        for s in sol:
            indexes = sorted(s.keys())
            print(tuple([s[i] for i in indexes]))
        print(len(sol))
    elif isinstance(sol, dict):
        indexes = sorted(sol.keys())
        print(tuple([sol[i] for i in indexes]))