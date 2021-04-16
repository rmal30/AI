from classes.search_query import SearchQuery
class Puzzle:
    
    def __init__(self, n):
        self.move_count = 0
        self.manhattan_count = 0
        self.n = n
        self.lower_limit = {"U": 0, "D": -n, "R": -1, "L": 0}
        self.upper_limit = {"U": n, "D": 0, "R": 0, "L": 1}
        self.diffs = {"U": n, "D": -n, "R": -1, "L": 1}
        self.total_dists = {}


        self.moveTable = []
        for i in range(n*n):
            self.moveTable.append(self.find_moves(i))

        self.distTable = {}
        for i in range(n*n):
            for j in range(n*n):
                self.distTable[(i, j)] = self.dist(i, j)

    def dist(self, pos1, pos2):
        n = self.n
        start_row = pos1 // n
        goal_row = pos2 // n
        start_col = pos1 % n
        goal_col = pos2 % n
        if start_row > goal_row:
            diff_row = start_row - goal_row
        else:
            diff_row = goal_row - start_row
        
        if start_col > goal_col:
            diff_col = start_col - goal_col
        else:
            diff_col = goal_col - start_col

        return diff_row + diff_col

    def manhattan_dist(self, state):
        n = self.n
        table = self.distTable
        empty_loc = state.index(n*n)
        return sum([table[(i, state[i] - 1)] for i in range(n*n)]) - table[(empty_loc, n*n - 1)]
    
    def total_dist(self, state):
        if not state in self.total_dists:
            n = self.n
            #table = self.distTable
            #empty_loc = state.index(n*n)
            
            #result = sum([table[(i, state[i] - 1)] for i in range(n*n)]) - table[(empty_loc, n*n - 1)]
            
            lc = 0
            for row in range(n):
                max=-1
                for col in range(n):
                    cellvalue = state[row*n + col]
                    if cellvalue != n*n and (cellvalue - 1) // n == row:
                        if cellvalue > max:
                            max = cellvalue
                        else:
                            lc += 1			

            for col in range(n):
                max=-1
                for row in range(n):
                    cellvalue = state[row*n + col]
                    if cellvalue != n*n and cellvalue % n == col + 1:
                        if cellvalue > max:
                            max = cellvalue
                        else:   
                            lc += 1
        

            self.total_dists[state] = 2*lc
        
        return self.total_dists[state]
        
    def get_parity(self, state):
        count = 0
        empty_loc = state.index(self.n * self.n)
        if self.n % 2 == 0:
            count += (empty_loc // self.n)
        state = state[:empty_loc] + state[empty_loc + 1:]
        for j in range(len(state)):
            for i in range(j):
                if state[i] > state[j]:
                    count += 1
        return count % 2

    def find_blank(self, state):
        n = self.n
        return state.index(n*n)

    def find_moves(self, empty_loc):
        n = self.n
        row = empty_loc // n
        col = empty_loc % n

        moves = []
        if row < n - 1:
            moves.append("U")
        
        if row > 0:
            moves.append("D")
        
        if col > 0:
            moves.append("R")

        if col < n - 1:
            moves.append("L")

        return moves

    def apply_move(self, boardArr, empty_loc, move):
        self.move_count += 1
        a = empty_loc + self.lower_limit[move]
        b = empty_loc + self.upper_limit[move]
        boardArr[a], boardArr[b] = boardArr[b], boardArr[a]
        result = tuple(boardArr)
        boardArr[a], boardArr[b] = boardArr[b], boardArr[a]
        return result

    def is_connected(self, state1, state2):
        return self.get_parity(state1) == self.get_parity(state2)




#24 moves
size = 3
start_node = (9, 3, 2, 8, 7, 1, 4, 5, 6)

#31 moves
#size = 3
#start_node = (8, 6, 7, 2, 5, 4, 3, 9, 1)

#40 moves
#size = 4
#start_node = (2, 7, 11, 5, 13, 16, 9, 4, 14, 1, 8, 6, 10, 3, 12, 15)

#46 moves
#size = 4
#start_node = (8, 6, 7, 2, 5, 4, 3, 9, 10, 11, 12, 1, 13, 14, 15, 16)

#47 moves
#size = 4
#start_node = (10, 8, 7, 2, 5, 4, 3, 9, 6, 11, 12, 1, 13, 14, 16, 15)

#80 moves
#size = 4
#start_node = (16, 12, 9, 13, 15, 11, 10, 14, 3, 7, 6, 2, 4, 8, 5, 1)

end_node = tuple(range(1, size * size + 1))

puzzle = Puzzle(size)

def next_neighbours(board):
    empty_loc = puzzle.find_blank(board)
    boardArr = list(board)
    moves = puzzle.moveTable[empty_loc]
    return [puzzle.apply_move(boardArr, empty_loc, move) for move in moves]

def next_edges(board):
    empty_loc = puzzle.find_blank(board)
    boardArr = list(board)
    moves = puzzle.moveTable[empty_loc]
    return [(1, puzzle.apply_move(boardArr, empty_loc, move)) for move in moves]


query = SearchQuery(start_node, end_node, get_neighbours = next_neighbours, get_edges = next_edges, heuristic_func = lambda x: puzzle.manhattan_dist(x) + puzzle.total_dist(x))