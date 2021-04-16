from classes.csp import CSP
tiles = {
    0: ("BH", "GH", "YH", "YH"),
    1: ("RT", "BT", "RH", "GT"),
    2: ("GH", "GT", "YT", "BH"),
    3: ("YT", "YT", "GT", "RT"),
    4: ("RT", "GH", "BH", "YH"),
    5: ("YH", "BT", "YT", "GT"),
    6: ("GH", "RH", "BT", "RH"),
    7: ("BT", "BH", "GH", "RT"),
    8: ("YH", "RH", "RT", "BT"),
}

problem = CSP({})

def rotateTile(angle, tile):
    return tile[-angle:] + tile[0: -angle]

def comparePatterns(p1, p2):
    return p1[0] == p2[0] and ((p1[1] == "H" and p2[1] == "T") or (p1[1] == "T" and p2[1] == "H"))

def edgeMatch(x, angle1, angle2):
    return len(x) < 4 or comparePatterns(rotateTile(x[2], tiles[x[0]])[angle1], rotateTile(x[3], tiles[x[1]])[angle2])

for i in range(9):
    problem.add_variable("O"+str(i), range(4))
    problem.add_variable("P"+str(i), range(9))


problem.add_constraint(("P0", "P1", "O0", "O1"), lambda x: edgeMatch(x, 1, 3))
problem.add_constraint(("P1", "P2", "O1", "O2"), lambda x: edgeMatch(x, 1, 3))

problem.add_constraint(("P3", "P4", "O3", "O4"), lambda x: edgeMatch(x, 1, 3))
problem.add_constraint(("P4", "P5", "O4", "O5"), lambda x: edgeMatch(x, 1, 3))

problem.add_constraint(("P6", "P7", "O6", "O7"), lambda x: edgeMatch(x, 1, 3))
problem.add_constraint(("P7", "P8", "O7", "O8"), lambda x: edgeMatch(x, 1, 3))

problem.add_constraint(("P0", "P3", "O0", "O3"), lambda x: edgeMatch(x, 2, 0))
problem.add_constraint(("P3", "P6", "O3", "O6"), lambda x: edgeMatch(x, 2, 0))

problem.add_constraint(("P1", "P4", "O1", "O4"), lambda x: edgeMatch(x, 2, 0))
problem.add_constraint(("P4", "P7", "O4", "O7"), lambda x: edgeMatch(x, 2, 0))

problem.add_constraint(("P2", "P5", "O2", "O5"), lambda x: edgeMatch(x, 2, 0))
problem.add_constraint(("P5", "P8", "O5", "O8"), lambda x: edgeMatch(x, 2, 0))

problem.add_constraint(tuple("P"+str(i) for i in range(9)), lambda x: len(x) == len(set(x)))

def show_solution(sol):
    if not isinstance(sol, list):
        sol = [sol]

    for s in sol:
        tiles_sol = []
        for key in range(9):
            tiles_sol += [rotateTile(s["O"+str(key)], tiles[s["P"+str(key)]])]
        print("".join("  " + tiles_sol[i][0] + "  " for i in range(3)))
        print("".join(tiles_sol[i][3] + "  " + tiles_sol[i][1] for i in range(3)))
        print("".join("  " + tiles_sol[i][2] + "  " for i in range(3)))
        print("".join("  " + tiles_sol[i][0] + "  " for i in range(3,6)))
        print("".join(tiles_sol[i][3] + "  " + tiles_sol[i][1] for i in range(3,6)))
        print("".join("  " + tiles_sol[i][2] + "  " for i in range(3,6)))
        print("".join("  " + tiles_sol[i][0] + "  " for i in range(6,9)))
        print("".join(tiles_sol[i][3] + "  " + tiles_sol[i][1] for i in range(6,9)))
        print("".join("  " + tiles_sol[i][2] + "  " for i in range(6,9)))
        print("")