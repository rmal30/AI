import math
from classes.game import Game

class AdversarialSearch:
    def __init__(self, game : Game):
        self.game = game

    def alpha_beta_search(self, state):
        (action, value) = self.max_value(state, -math.inf, math.inf)
        return (action, value)

    def max_value(self, state, alpha, beta):
        if self.game.terminal(state):
            return (None, self.game.utility(state))

        opts = {a: -self.max_value(self.game.move(state,a), alpha, beta)[1] for a in self.game.actions(state)}
        k = max(opts, key=opts.get)
        if opts[k] >= beta:
            return (k, opts[k])
        alpha = max(alpha, opts[k])
        return (k, opts[k])