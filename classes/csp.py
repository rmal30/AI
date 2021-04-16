def revise_domain(csp, init, vars):
    for var in init:
        if var in vars:
            for var2 in vars:
                if var2 != var:
                    csp.domains[var2].discard(init[var])

class CSP:
    def __init__(self, init):
        self.vars = set()
        self.domains = {}
        self.constraints = {}
        self.scopes = {}
        self.init = init
        self.heuristics = {}
        self.use_min_remaining_heuristic = False
        self.require_all_variables = False

    def add_variable(self, var, domain):
        self.vars.add(var)
        self.domains[var] = set(domain)

    def add_constraint(self, vars, func):
        revise_domain(self, self.init, vars)
        self.constraints[tuple(vars)] = func
        for var in vars:
            if var not in self.scopes:
                self.scopes[var] = []
            self.scopes[var].append(tuple(vars))
            len_scopes = {i: len(i) for i in self.scopes[var]}
            self.scopes[var] = sorted(len_scopes, key=len_scopes.get, reverse=True)

    def add_heuristic(self, vars, func):
        self.heuristics[tuple(vars)] = func
