"""
The Englishman lives in the red house.
The Spaniard owns the dog.
Coffee is drunk in the green house.
The Ukrainian drinks tea.

The green house is immediately to the right of the ivory house.
The Old Gold smoker owns snails.
Kools are smoked in the yellow house.
Milk is drunk in the middle house.

The Norwegian lives in the first house.
The man who smokes Chesterfields lives in the house next to the man with the fox.
Kools are smoked in the house next to the house where the horse is kept.
The Lucky Strike smoker drinks orange juice.
The Japanese smokes Parliaments.
The Norwegian lives next to the blue house.
"""
from classes.csp import CSP

nationalities = ("Englishman", "Spaniard", "Norwegian", "Japanese", "Ukrainian", )
drinks = ("Coffee", "Milk", "Orange juice", "Tea", "Water")
smokes = ("Old Gold", "Kools", "Chesterfields", "Lucky Strike", "Parliaments")
colors = ("Red", "Green", "Ivory", "Yellow", "Blue")
animals = ("Dog", "Snails", "Fox", "Horse", "Zebra")

properties = (colors, nationalities, drinks, smokes, animals)

problem = csp.CSP({nationalities[2]: 0, drinks[1]: 2})

for prop in properties:
    for i in prop:
        problem.add_variable(i, range(5))

problem.add_constraint((nationalities[0], colors[0]), lambda x: len(x) == 1 or x[0] == x[1])
problem.add_constraint((nationalities[1], animals[0]), lambda x: len(x) == 1 or x[0] == x[1])
problem.add_constraint((drinks[0], colors[1]), lambda x: len(x) == 1 or x[0] == x[1])

problem.add_constraint((nationalities[4], drinks[3]), lambda x: len(x) == 1 or x[0] == x[1])
problem.add_constraint((colors[1], colors[2]), lambda x: len(x) == 1 or x[0] == x[1] + 1)
problem.add_constraint((smokes[0], animals[1]), lambda x: len(x) == 1 or x[0] == x[1])
problem.add_constraint((smokes[1], colors[3]), lambda x: len(x) == 1 or x[0] == x[1])

problem.add_constraint((smokes[2], animals[2]), lambda x: len(x) == 1 or abs(x[0] - x[1]) == 1)
problem.add_constraint((smokes[1], animals[3]), lambda x: len(x) == 1 or abs(x[0] - x[1]) == 1)
problem.add_constraint((smokes[3], drinks[2]), lambda x: len(x) == 1 or x[0] == x[1])
problem.add_constraint((smokes[4], nationalities[3]), lambda x: len(x) == 1 or x[0] == x[1])
problem.add_constraint((nationalities[2], colors[4]), lambda x: len(x) == 1 or abs(x[0] - x[1]) == 1)
problem.add_constraint(nationalities, lambda x: len(x) == len(set(x)))
problem.add_constraint(drinks, lambda x: len(x) == len(set(x)))
problem.add_constraint(smokes, lambda x: len(x) == len(set(x)))
problem.add_constraint(colors, lambda x: len(x) == len(set(x)))
problem.add_constraint(animals, lambda x: len(x) == len(set(x)))

def show_sol(sol):
    for prop in properties:
        prop_sol = {k: sol[k] for k in sol if k in prop}
        result = sorted(prop_sol, key=prop_sol.get)
        print("".join([x.center(15) for x in result]))


def show_solution(sol):
    if isinstance(sol, list):
        for s in sol:
            show_sol(s)
    else:
        show_sol(sol)


