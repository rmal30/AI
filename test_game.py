from games.tictactoe import game
from algo.adversarial_search import AdversarialSearch
a = AdversarialSearch(game)
state = game.init
while not game.terminal(state):
    (opt, val) = a.alpha_beta_search(state)
    state = game.move(state, opt)
    print(state)
    if game.terminal(state):
        break
    player_move = input()
    state = game.move(state, int(player_move))