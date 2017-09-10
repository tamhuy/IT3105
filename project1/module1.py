def loadBoard(filename): #Function to read from file
    f = open(filename, 'r')
    board = [['x' for _ in range(6)] for _ in range(6)]
    state = []
    for line in f:
        state.append([int(s) for s in line.split(',')])

    print state


    print board
    for line in state:
        print "car:", state.index(line)
        print line[1], line[2]
        board[line[1]][line[2]] = state.index(line)

        for i in range(line[3]):
            print i
            if line[0] == 0:
                board[line[1] + i][line[2]] = state.index(line)
            else:
                board[line[1]][line[2] + i] = state.index(line)
    f.close()
    return board

def printBoard(board):
    for i in range(6):
        x = ''
        for j in range(6):
            x += str(board[j][i])
        print x

def run():
    filename = "module1/Scenarios/easy-3.txt"
    board = loadBoard(filename)
    printBoard(board)

run()