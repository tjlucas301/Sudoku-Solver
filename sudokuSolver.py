N = 3

# loads the sudoku board from the given file
def loadSudoku(filename):
    start_state = []
    with open(filename, 'r') as file:
        for line in file:
            start_state.append([int(i) for i in line.split()])
    return start_state

s1 = loadSudoku("sudoku0.txt")
s2 = loadSudoku("sudoku1.txt")

##########################################
####   Utility Functions
##########################################

# converts a given row and column to its inner box number
def spaceToBox(space):
    return N * (space[0] // N) + space[1] // N

# Returns the set of the values currently in the corresponding row on the board
def valsInRow(board, row):
    return set(board[row][col] for col in range(N * N) if board[row][col] != 0)

# Returns the set of the values currently in the corresponding column on the board
def valsInCol(board, col):
    return set(board[row][col] for row in range(N * N) if board[row][col] != 0)

# Returns the set of the values currently in the corresponding box on the board
def valsInBox(board, box):
    #box = spaceToBox(space)
    row = N * (box // N)
    col = N * (box % N)
    return set(board[r][c] for r in range(row, row + 3) for c in range(col, col + 3) if board[r][c] != 0)

# Returns the set of the cells in a row currently constrained by the cells in the corresponding row on the board
def constraintsInRow(board, row):
    return set((row, col) for col in range(N * N) if board[row][col] == 0)

# Returns the set of the cells in a column currently constrained by the cells in the corresponding column on the board
def constraintsInCol(board, col):
    return set((row, col) for row in range(N * N) if board[row][col] == 0)

# Returns the set of the cells in a box currently constrained by the cells in the corresponding box on the board
def constraintsInBox(board, space):
    box = spaceToBox(space)
    row = N * (box // N)
    col = N * (box % N)
    return set((r, c) for r in range(row, row + 3) for c in range(col, col + 3) if board[r][c] == 0)

# Returns a set of all variables that are unassigned
def unassignedVariables(board):
    variables = []
    for row in range(N*N):
        for col in range(N*N):
            if board[row][col] == 0:
                variables.append((row, col))
    return set(variables)

# makes a move: Fills the given value in the given space within the board
def makeMove(board, space, value):
    new_board = []
    for r in range(N*N):
        row = []
        for c in range(N*N):
            row.append(board[r][c])
        new_board.append(row)
    new_board[space[0]][space[1]] = value
    return new_board

# returns True if the space is empty and on the board,
# and assigning value to it if not blocked by any constraints

def isValidMove(board, space, value):
    if ((board[space[0]][space[1]] != 0) | (value in valsInRow(board, space[0]))|
            (value in valsInCol(board, space[1])) | (value in valsInBox(board, spaceToBox(space)))):
        return False
    return True

def is_goal(board):
    for row in range(N * N):
        for col in range(N * N):
            if board[row][col] == 0:
                return False
    return True

# Minimum remaining values heuristic
def mrv(board):
    domains = []
    for pos in unassignedVariables(board):
        domain_values = [pos]
        values = []
        for i in range(1, 10):
            if isValidMove(board, pos, i):
                values.append(i)
        domain_values.append(values)
        domains.append(domain_values)
    domains = sorted(domains, key=lambda x: len(x[1]))
    return domains

def solveBoard(board):
    pos_dom = mrv(board) # Look at the domain of every unassigned position, and sort positions according to those with least remaining elements in domain
    curr_pos = pos_dom[0]
    pos = curr_pos[0]
    vals = curr_pos[1] # curr_pos is the first element in pos_dom, pos is the position, and vals are the elements in the domain
    
    # Pick position for next move
    for value in vals:  # For each possible value
        new_board = makeMove(board, pos, value)  
        if is_goal(new_board):
            return new_board  # If goal state, return
        
        next_state = solveBoard(new_board)
        if next_state and is_goal(next_state):
            return next_state  # If goal state, return

    return board

# prints out a command line representation of the board

def printBoard(board):
    for r in range(N * N):
        # add row divider
        if r % N == 0 and not r == 0:
            print("-----------------------------")
        row = ""
        for c in range(N * N):
            val = board[r][c]
            # add column divider
            if c % N == 0 and not c == 0:
                row += " | "
            else:
                row += "  "
            # add value placeholder
            row += str(val)
        print(row)

printBoard(solveBoard(s1))
print("\n")
printBoard(solveBoard(s2))


