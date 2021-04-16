import random
import math

def get_scope_values(vals, scope):
    return tuple(vals[var] for var in scope if var in vals)

class ConstraintSolver:
    def __init__(self, csp):
        self.csp = csp

    def check_assignment(self, vals, var = None):
        constraints = self.csp.constraints if var is None else self.csp.scopes[var]
        return all(self.csp.constraints[scope](get_scope_values(vals, scope)) for scope in constraints)

    def infer(self, vals, domains, var):
        scopes = self.csp.scopes[var]
        values = {}
        for scope in scopes:
            values[scope] = get_scope_values(vals, scope)
            if not self.csp.constraints[scope](values[scope]):
                return None

        new_domains = domains.copy()
        for scope in scopes:
            if not self.csp.require_all_variables or len(values[scope]) + 1 == len(scope):
                remaining = [i for i in scope if i not in vals] 
                if remaining:
                    unknown = remaining[0]
                    satisfies = []
                    new_vals = vals.copy()
                    for domain in new_domains[unknown]:
                        new_vals[unknown] = domain
                        if self.csp.constraints[scope](tuple(new_vals[i] for i in scope if i in vals or i == unknown)):
                            satisfies.append(domain)
                    new_domains[unknown] = satisfies
                    satisfies_count = len(satisfies)
                    if satisfies_count == 0:
                        return None
                    elif satisfies_count == 1:
                        vals[unknown] = satisfies[0]
                        new_domains[unknown] = [satisfies[0]]
                        return self.infer(vals, new_domains, unknown)

        return (vals, new_domains)

    def get_next_iteration(self, var, assignments):
        new_states = []
        sols = []
        for (assignment, domains) in assignments:
            if var in assignment:
                new_states.append((assignment, domains))
            else:
                for v in domains[var]:
                    assignment2 = assignment.copy()
                    domains2 = domains.copy()
                    assignment2[var] = v
                    domains2[var] = [v]
                    inference = self.infer(assignment2, domains2, var)
                    if inference is not None:
                        (assignment2, domains2) = inference
                        if len(assignment2) == len(self.csp.vars):
                            sols.append(assignment2)
                        else:
                            new_states.append((assignment2, domains2))
        print(var, len(new_states))
        return new_states, sols

    def get_all_solutions(self):
        assignments = [(self.csp.init, self.csp.domains)]
        sols = []
        for var in self.csp.vars:
            if var not in self.csp.init:
                assignments, new_sols = self.get_next_iteration(var, assignments)
                sols += new_sols
        return sols

    def get_one_solution(self):
        if self.csp.use_min_remaining_heuristic:
            return self.min_remaining_backtrack(self.csp.init)
        else:
            return self.backtrack(self.csp.init, self.csp.domains)
    
    def backtrack(self, assignment, domains):
        unassigned = [var for var in self.csp.vars if var not in assignment]
        if not unassigned:
            return assignment
        var = unassigned[0]
        for v in domains[var]:
            domains2 = domains.copy()
            assignment2 = assignment.copy()
            assignment2[var] = v
            sat = self.infer(assignment2, domains2, var)
            if sat is not None:
                (new_assignment, new_domain) = sat
                result = self.backtrack(new_assignment, new_domain)
                if result is not None:
                    return result
        return None

    def get_remaining(self, assignment, var):
        remaining = set(self.csp.domains[var])
        for scope in self.csp.scopes[var]:
            values = [assignment[var] for var in scope if var in assignment]
            remaining -= set(val for val in list(remaining) if not self.csp.constraints[scope](values + [val]))
        return remaining
    
    def min_remaining_backtrack(self, assignment):
        unassigned = [var for var in self.csp.vars if var not in assignment]
        if not unassigned:
            return assignment

        dic = {x: self.get_remaining(assignment, x) for x in unassigned}
        dic2 = {x: len(dic[x]) for x in dic}
        i = min(dic2, key=dic2.get)

        if dic2[i] == 0:
            return None

        for j in dic[i]:
            assignment[i] = j
            result = self.min_remaining_backtrack(assignment)
            if result is not None:
                return result

        del assignment[i]
        return None

    def count_conflicts(self, vals, var):
        vars = set(vals.keys())
        total = 0
        for scope in self.csp.scopes[var]:
            common = set(scope).intersection(vars)
            values = [vals[i] for i in common]
            total += self.csp.heuristics[scope](values)
        return total

    def min_conflicts(self, max_steps=100000):
        current = {i: random.sample(self.csp.domains[i], 1)[0] for i in self.csp.vars}
        count = 0
        for i in range(max_steps):
            conflicts = []
            for scope in self.csp.constraints:
                common = set(scope).intersection(self.csp.vars)
                if not self.csp.constraints[scope]([current[i] for i in common]):
                    conflicts += scope

            if conflicts:
                var = random.sample(conflicts, 1)[0]
                old_j = current[var]
                min_conflicts = self.count_conflicts(current, var)
                min_j = [old_j]
                for j in self.csp.domains[var]:
                    current[var] = j
                    con = self.count_conflicts(current, var)
                    if con <= min_conflicts and j != old_j:
                        if con < min_conflicts:
                            min_j = [j]
                            min_conflicts = con
                        elif con == min_conflicts:
                            min_j += [j]
                current[var] = random.sample(min_j, 1)[0]
            else:
                print(count)
                return current
            count += 1
        print(count)
        return None