import worlds.wumpus as world

state = world.environment()

print(world.performance(state))

end = False
while not end:
    actions = world.get_actions(state)
    sensors = world.sensors(state)
    if not actions:
        end = True
        continue
    print(actions, sensors)
    print(state["player"])
    chosen_action = input("Choose action: ")

    options = {
        "L": "LEFT",
        "R": "RIGHT",
        "F": "FORWARD",
        "S": "SHOOT",
        "G": "GRAB",
        "C": "CLIMB"
    }

    state = world.apply_action(state, options[chosen_action])
    print(world.performance(state))

print(state)