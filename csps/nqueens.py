from classes.csp import CSP

N = 10

def queen_constraint(vals):
    cols = [val[0] for val in vals]
    rows = [val[1] for val in vals]
    if len(rows) != len(set(rows)) or len(cols) != len(set(cols)):
        return False
    diag1 = [cols[i] + rows[i] for i in range(len(vals))]
    diag2 = [cols[i] - rows[i] for i in range(len(vals))]
    return len(diag1) == len(set(diag1)) and len(diag2) == len(set(diag2))

def queen_heuristic(vals):
    cols = [val[0] for val in vals]
    rows = [val[1] for val in vals]
    diag1 = [cols[i] + rows[i] for i in range(len(vals))]
    diag2 = [cols[i] - rows[i] for i in range(len(vals))]
    return len(diag1) - len(set(diag1)) + len(diag2) - len(set(diag2)) + len(rows) - len(set(rows)) + len(cols) - len(set(cols))

problem = CSP({})
for i in range(N):
    problem.add_variable(i, [(i, j) for j in range(N)])

problem.add_constraint(range(N), queen_constraint)
problem.add_heuristic(range(N), queen_heuristic)

problem.use_min_remaining_heuristic = True

def show_solution(sol):
    if isinstance(sol, list):
        for s in sol:
            print(s)
        print(len(sol))
    elif isinstance(sol, dict):
        print(tuple(sol.values()))