from classes.game import Game

def gen_wins(N):
    wins = []
    for i in range(N):
        wins.append(range(i * N, i * N + N))
        wins.append(range(i, i + N * (N - 1) + 1, N))
    wins.append(range(0, N * N, N + 1))
    wins.append(range(N - 1, N * N - N + 1, N - 1))
    return wins

WINS = gen_wins(3)

def is_win(state, player):
    return any(set(win).issubset(state[player]) for win in WINS)

def utility(state, player):
    if is_win(state, player):
        return +1

    if is_win(state, 1 - player):
        return -1

    return 0

def make_move(state, player, pos):
    new_state = {}
    new_state[0] = state[0].copy()
    new_state[1] = state[1].copy()
    new_state[player].add(pos)
    return new_state

def get_moves(state, player):
    N = 3
    existing_plays = set.union(state[player], state[1 - player])
    return [i for i in range(N * N) if i not in existing_plays]

def get_turn(state):
    if len(state[0]) <= len(state[1]):
        return 0
    else:
        return 1

utility_func = lambda state: utility(state, get_turn(state))
actions_func = lambda state: get_moves(state, get_turn(state))
move_func = lambda state, pos: make_move(state, get_turn(state), pos)
terminal_func = lambda state: utility_func(state) != 0 or actions_func(state) == []

game = Game(
    initial = {0: set(), 1: set()}, 
    utility = utility_func,
    actions = actions_func,
    move = move_func,
    terminal = terminal_func
)