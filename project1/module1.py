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
    return board, state

def printBoard(board):
    for i in range(6):
        x = ''
        for j in range(6):
            x += str(board[j][i])
        print x

def findLegalMoves(board, state):
    validStates = []
    for car in state:
        print "car ", state.index(car)
        if car[0] == 0:
            if board[car[1] - 1][car[2]] == 'x' and car[1] != 0: # Check to see if the car can move to the left
                print "valid"
                tempState = state[:]
                tempState[state.index(car)] = [car[0], car[1] - 1, car[2], car[3]]
                print tempState
                validStates.append(tempState)
                #validMove.append([car[0], car[1] - 1, car[2], car[3]])

            if car[1]+car[3] < 6:
                if board[(car[1] + car[3])][car[2]] == 'x' : # Check to see if the car can move to the right
                    print "valid"
                    tempState = state[:]
                    tempState[state.index(car)] = [car[0], car[1] + 1, car[2], car[3]]
                    validStates.append(tempState)

        else:
            if board[car[1]][car[2] -1] == 'x' and car[2] != 0: # check to see if the car can move up
                print "valid"
                tempState = state[:]
                tempState[state.index(car)] = [car[0], car[1] , car[2]-1, car[3]]
                validStates.append(tempState)
            if car[2] + car[3] < 6:
                if board[car[1]][car[2] + car[3]] == 'x': # check to see if the car can move up
                    print "valid"
                    tempState = state[:]
                    tempState[state.index(car)] = [car[0], car[1] , car[2]+1, car[3]]
                    validStates.append(tempState)
    '''
    print "0", validStates[0]
    print "1", validStates[1]
    print "2", validStates[2]
    
    '''
    for i in validStates:
        print i



def run():
    filename = "module1/Scenarios/easy-3.txt"
    board, state = loadBoard(filename)
    printBoard(board)
    findLegalMoves(board,state)
run()