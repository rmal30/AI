import random
START = (1, 1)
DIRECTIONS = ((1, 0), (0, -1), (-1, 0), (0, 1))
N = 4

def performance(state):
    score = 0
    if ("gold" not in state) and ("player" not in state) and state["alive"]:
        score += 1000
    
    if "player" in state and ((state["player"] in state["pits"]) or (state["player"] == state["wumpus"] and not state["wumpusKilled"])):
        score -= 1000
    
    if state["arrows"] == 0:
        score -= 10
    
    score -= state["moveCount"]
    return score

def environment():
    state = {}

    state["hit"] = False
    state["scream"] = False
    state["wumpusKilled"] = False
    state["player"] = START
    state["pits"] = []
    state["arrows"] = 1
    state["moveCount"] = 0
    state["alive"] = True
    state["direction"] = DIRECTIONS[0]

    for i in range(1, N+1):
        for j in range(1, N+1):
            a = random.random()
            if a < 0.2 and (i, j) != START:
                state["pits"].append((i,j))

    while ("gold" not in state) or state["gold"] == START or state["gold"] in state["pits"]:
        state["gold"] = (random.randint(1, N), random.randint(1, N))
    
    while ("wumpus" not in state) or (state["wumpus"] == START) or state["wumpus"] in state["pits"]:
        state["wumpus"] = (random.randint(1, N), random.randint(1, N))
    
    return state

def get_actions(state):
    moves = set()
    if state["alive"] and "player" in state:
        moves.add("LEFT")
        moves.add("RIGHT")
        moves.add("FORWARD")

        if state["arrows"] >= 1:
            moves.add("SHOOT")

        if "gold" in state and state["gold"] == state["player"]:
            moves.add("GRAB")

        if state["player"] == START:
            moves.add("CLIMB")

    return moves

def apply_action(state, move):
    state["hit"] = False
    state["scream"] = False
    state["moveCount"] += 1

    if move == "FORWARD":
        new_pos = (state["player"][0] + state["direction"][0], state["player"][1] + state["direction"][1])
        if new_pos[0] < 1 or new_pos[0] > N or new_pos[1] < 1 or new_pos[1] > N:
            state["hit"] = True
        else:
            state["player"] = new_pos
            if new_pos == state["wumpus"] and not state["wumpusKilled"]:
                state["alive"] = False
            
            if new_pos in state["pits"]:
                state["alive"] = False

    if move == "LEFT":
        state["direction"] = DIRECTIONS[(DIRECTIONS.index(state["direction"]) - 1) % 4]
    
    if move == "RIGHT":
        state["direction"] = DIRECTIONS[(DIRECTIONS.index(state["direction"]) + 1) % 4]
    
    if move == "SHOOT": 
        state["arrows"] -= 1
        x_delta = (state["wumpus"][0] - state["player"][0]) * state["direction"][0]
        y_delta = (state["wumpus"][1] - state["player"][1]) * state["direction"][1]
        if (x_delta > 0 and y_delta == 0) or (y_delta > 0 and x_delta == 0):
            state["wumpusKilled"] = True
            state["scream"] = True
    
    if move == "GRAB":
        del state["gold"]

    if move == "CLIMB":
        del state["player"]

    return state

def dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def sensors(state):
    sensors = set()
    if "player" in state:
        if dist(state["player"], state["wumpus"]) <= 1:
            sensors.add("STENCH")
        if any(dist(state["player"], i) == 1 for i in state["pits"]):
            sensors.add("BREEZE")
        if "gold" in state and state["player"] == state["gold"]:
            sensors.add("GLITTER")
        if state["hit"]:
            sensors.add("BUMP")
        if state["scream"]:
            sensors.add("SCREAM")
    
    return sensors