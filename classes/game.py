class Game:
    def __init__(self, initial, utility, actions, move, terminal):
        self.init = initial
        self.utility = utility
        self.actions = actions
        self.move = move
        self.terminal = terminal