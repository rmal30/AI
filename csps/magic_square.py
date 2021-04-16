from classes.csp import CSP

def magic_constraint(vals):
    count = len(vals)
    total = sum(vals)
    expected_sum = N*(N*N+1)/2
    if count == N:
        return total == expected_sum
    elif count == N - 1:
        return total >= expected_sum - N*N and total < expected_sum
    else:
        return total < expected_sum

def alldiff(vals):
    return len(vals) == len(set(vals))

N = 4
problem = CSP({})
for i in range(N*N):
    problem.add_variable(i, range(1, N*N + 1))

problem.add_constraint(range(N*N), alldiff)

for i in range(N):
    problem.add_constraint(range(i*N, i*N + N), magic_constraint)
    problem.add_constraint(range(i, i + N*(N - 1) + 1, N), magic_constraint)

problem.add_constraint(range(0, N*N, N + 1), magic_constraint)
problem.add_constraint(range(N - 1, N*N - N + 1, N - 1), magic_constraint)

if N == 4:
    lines = [
        (0, 3, 12, 15), (5, 6, 9, 10), (1, 2, 13, 14), (4, 8, 7, 11),
        (0, 1, 4, 5), (2, 3, 6, 7), (8, 9, 12, 13), (10, 11, 14, 15),
        (1, 6, 11, 12), (2, 7, 8, 13), (3, 4, 9, 14),
        (0, 7, 10, 13), (1, 4, 11, 14), (2, 5, 8, 15)
    ]
    for line in lines:
        problem.add_constraint(line, magic_constraint)
problem.require_all_variables = True

def show_solution(sol):
    if isinstance(sol, list):
        for s in sol:
            indexes = sorted(s.keys())
            print(tuple([s[i] for i in indexes]))
        print(len(sol))
    elif isinstance(sol, dict):
        print(tuple(sol.values()))