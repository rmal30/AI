from classes.csp import CSP
from enum import Enum

class CenterFish(Enum):
    OR, BL, PU, GR, ZE, PF = range(6)
    
class SideFish(Enum):
    GR, BY, WB, OS, OR = range(5)

tiles = {
    0: (CenterFish.GR, (SideFish.BY, SideFish.GR, SideFish.OR, SideFish.WB)),
    1: (CenterFish.GR, (SideFish.OR, SideFish.OS, SideFish.BY, SideFish.GR)),
    2: (CenterFish.GR, (SideFish.GR, SideFish.OS, SideFish.BY, SideFish.WB)),
    3: (CenterFish.GR, (SideFish.WB, SideFish.OS, SideFish.GR, SideFish.OR)),
    4: (CenterFish.GR, (SideFish.WB, SideFish.GR, SideFish.OS, SideFish.OR)),
    5: (CenterFish.GR, (SideFish.GR, SideFish.BY, SideFish.OS, SideFish.WB)),
    6: (CenterFish.ZE, (SideFish.GR, SideFish.OS, SideFish.BY, SideFish.OR)),
    7: (CenterFish.ZE, (SideFish.OR, SideFish.GR, SideFish.WB, SideFish.OS)),
    8: (CenterFish.PF, (SideFish.BY, SideFish.WB, SideFish.GR, SideFish.OS)),
    9: (CenterFish.PU, (SideFish.GR, SideFish.BY, SideFish.WB, SideFish.OS)),
    10: (CenterFish.PU, (SideFish.BY, SideFish.OS, SideFish.WB, SideFish.GR)),
    11: (CenterFish.PU, (SideFish.WB, SideFish.BY, SideFish.GR, SideFish.OS)),
    12: (CenterFish.ZE, (SideFish.WB, SideFish.OR, SideFish.GR, SideFish.OS)),
    13: (CenterFish.PU, (SideFish.BY, SideFish.GR, SideFish.WB, SideFish.OS)),
    14: (CenterFish.OR, (SideFish.OS, SideFish.BY, SideFish.GR, SideFish.OR)),
    15: (CenterFish.PU, (SideFish.BY, SideFish.OR, SideFish.OS, SideFish.GR)),
    16: (CenterFish.PF, (SideFish.OR, SideFish.OS, SideFish.GR, SideFish.BY)),
    17: (CenterFish.BL, (SideFish.GR, SideFish.OR, SideFish.BY, SideFish.OS)),
    18: (CenterFish.BL, (SideFish.BY, SideFish.WB, SideFish.GR, SideFish.OR)),
    19: (CenterFish.BL, (SideFish.BY, SideFish.GR, SideFish.WB, SideFish.OR)),
    20: (CenterFish.PF, (SideFish.OS, SideFish.WB, SideFish.BY, SideFish.GR)),
    21: (CenterFish.PU, (SideFish.OS, SideFish.OR, SideFish.BY, SideFish.GR)),
    22: (CenterFish.ZE, (SideFish.OS, SideFish.GR, SideFish.OR, SideFish.BY)),
    23: (CenterFish.BL, (SideFish.WB, SideFish.OR, SideFish.OS, SideFish.GR)),
    24: (CenterFish.BL, (SideFish.BY, SideFish.WB, SideFish.OS, SideFish.GR)),
    25: (CenterFish.PF, (SideFish.GR, SideFish.WB, SideFish.BY, SideFish.OS)),
    26: (CenterFish.PF, (SideFish.OS, SideFish.WB, SideFish.GR, SideFish.OR)),
    27: (CenterFish.OR, (SideFish.OS, SideFish.WB, SideFish.GR, SideFish.OR)),
    28: (CenterFish.ZE, (SideFish.OS, SideFish.OR, SideFish.GR, SideFish.BY)),
    29: (CenterFish.OR, (SideFish.WB, SideFish.OR, SideFish.BY, SideFish.GR)),
    30: (CenterFish.PF, (SideFish.GR, SideFish.WB, SideFish.BY, SideFish.OR)),
    31: (CenterFish.OR, (SideFish.OR, SideFish.GR, SideFish.WB, SideFish.BY)),
    32: (CenterFish.OR, (SideFish.GR, SideFish.OR, SideFish.BY, SideFish.WB)),
    33: (CenterFish.BL, (SideFish.WB, SideFish.OR, SideFish.GR, SideFish.BY)),
    34: (CenterFish.ZE, (SideFish.GR, SideFish.BY, SideFish.OR, SideFish.WB)),
    35: (CenterFish.OR, (SideFish.BY, SideFish.GR, SideFish.OS, SideFish.WB))
}

problem = CSP({})

def edgeMatch(x, angle1, angle2):
    return len(x) < 2 or tiles[x[0]][1][angle1].value == tiles[x[1]][1][angle2].value

order = [0, 1, 7, 6, 12, 13, 14, 8, 2, 3, 9, 15, 21, 20, 19, 18, 24, 25, 26, 27, 28, 22, 16, 10, 4, 5, 11, 17, 23, 29, 35, 34, 33, 32, 31, 30]

for i in order:
    problem.add_variable("P" + str(i), range(36))

for i in range(5):
    for j in range(6):
        problem.add_constraint(("P" + str(i + j*6), "P" + str((i + 1) + j*6)), lambda x: edgeMatch(x,3,1))
        problem.add_constraint(("P" + str(i*6 + j), "P" + str((i + 1)*6 + j)), lambda x: edgeMatch(x,0,2))

for i in range(6):
    problem.add_constraint(tuple("P" + str(k) for k in range(i*6, i*6 + 6)), lambda x: len(x) == len(set(tiles[t][0].value for t in x)))
    problem.add_constraint(tuple("P" + str(k) for k in range(i, 36 + i, 6)), lambda x: len(x) == len(set(tiles[t][0].value for t in x)))

problem.add_constraint(tuple("P" + str(k) for k in range(0, 42, 7)), lambda x: len(x) == len(set(tiles[t][0].value for t in x)))
problem.add_constraint(tuple("P" + str(k) for k in range(5, 35, 5)), lambda x: len(x) == len(set(tiles[t][0].value for t in x)))

problem.add_constraint(tuple("P" + str(i) for i in range(36)), lambda x: len(x) == len(set(x)))

def show_solution(sol):
    if not isinstance(sol, list):
        sol = [sol]

    for s in sol:
        tiles_sol = []
        for key in range(36):
            tiles_sol += [tiles[s["P" + str(key)]]]
        
        for i in range(6):
            print (" ".join("   " + str(tiles_sol[i][1][2].name) + "   " for i in range(6*i, 6*(i + 1))))
            print (" ".join(str(tiles_sol[i][1][1].name) + " " + str(tiles_sol[i][0].name) + " " + str(tiles_sol[i][1][3].name) for i in range(6*i, 6*(i + 1))))
            print (" ".join("   " + str(tiles_sol[i][1][0].name) + "   " for i in range(6*i, 6*(i + 1))))