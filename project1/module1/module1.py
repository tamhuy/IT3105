import aStar
#import GUI
import numpy as np
import matplotlib.pyplot as plt

class State:
    f = float("inf")
    g = None
    h = None
    parent = None
    children = []
    state = []
    board = []

    def __init__(self, state):  # Initialize a node with coordinates, type of character and weight
        board = [['.' for _ in range(6)] for _ in range(6)]
        self.state = state
        for line in state:
            #print "____________"
            #print self.board
            # print "car:", state.index(line)
            # print line[1], line[2]
            board[line[1]][line[2]] = state.index(line)
            #print board
            for i in range(line[3]):
               #print i
                if line[0] == 0:
                    board[line[1] + i][line[2]] = state.index(line)
                else:
                    board[line[1]][line[2] + i] = state.index(line)
        #print board
        self.board = board

    def heuristic(self):
        h = 6 - (self.state[0][1] + self.state[0][3])
        #print h
        h1 = 0
        #for i in range(h):
        if self.state[0][1]+self.state[0][3]-1 != 5:
            for i in range(h):
                #print self.board[self.state[0][1]+self.state[0][3]]
                if self.board[self.state[0][1]+self.state[0][3]+i][self.state[0][2]] != '.':
                    h1 += 1
                    a = self.board[self.state[0][1]+self.state[0][3]+i][self.state[0][2]]
                    if self.board[self.state[a][1]][self.state[a][2]-1] != '.' and self.board[self.state[a][1]][self.state[a][2] +self.state[a][3]] != '.':
                        h1 += 1
        return h + h1

    def isSolution(self):
        if self.state[0][1] + self.state[0][3] -1 == 5 and self.state[0][2] == 2:
            return True

    def findLegalMoves(self):
        validStates = []
        for car in self.state:
            # print "car ", self.state.index(car)
            if car[0] == 0:
                if self.board[car[1] - 1][car[2]] == '.' and car[1] != 0:  # Check to see if the car can move to the left
                    # print "valid"
                    tempState = self.state[:]
                    tempState[self.state.index(car)] = [car[0], car[1] - 1, car[2], car[3]]
                    # print tempState
                    validStates.append(State(tempState))
                    # validMove.append([car[0], car[1] - 1, car[2], car[3]])

                if car[1] + car[3] < 6:
                    if self.board[(car[1] + car[3])][car[2]] == '.':  # Check to see if the car can move to the right
                        # print "valid"
                        tempState = self.state[:]
                        tempState[self.state.index(car)] = [car[0], car[1] + 1, car[2], car[3]]
                        validStates.append(State(tempState))

            else:
                if self.board[car[1]][car[2] - 1] == '.' and car[2] != 0:  # check to see if the car can move up
                    # print "valid"
                    tempState = self.state[:]
                    tempState[self.state.index(car)] = [car[0], car[1], car[2] - 1, car[3]]
                    validStates.append(State(tempState))
                if car[2] + car[3] < 6:
                    if self.board[car[1]][car[2] + car[3]] == '.':  # check to see if the car can move up
                        # print "valid"
                        tempState = self.state[:]
                        tempState[self.state.index(car)] = [car[0], car[1], car[2] + 1, car[3]]
                        validStates.append(State(tempState))
        '''
        print "0", validStates[0]
        print "1", validStates[1]
        print "2", validStates[2]

        '''
        # for i in validStates:
        #    print i.state
        # print validStates[0].state
        return validStates

    def printBoard(self):
        for i in range(6):
            x = ''
            for j in range(6):
                x += str(self.board[j][i])
            print x
    def gui(self):
        GUI(self)


def loadBoard(filename):  # Function to read from file
    f = open(filename, 'r')
    board = [['.' for _ in range(6)] for _ in range(6)]
    state = []
    for line in f:
        state.append([int(s) for s in line.split(',')])

    # print state

    # print board
    '''
    for line in state:
        #print "car:", state.index(line)
        #print line[1], line[2]
        board[line[1]][line[2]] = state.index(line)

        for i in range(line[3]):
            #print i
            if line[0] == 0:
                board[line[1] + i][line[2]] = state.index(line)
            else:
                board[line[1]][line[2] + i] = state.index(line)

    '''
    f.close()
    return state


def printBoard(board):
    for i in range(6):
        x = ''
        for j in range(6):
            x += str(board[j][i])
        print x

class GUI():
    def __init__(self, node):
        self.image = self.initImage(node)

    def initImage(self, node):
        if GUI:
            board = self.visualize(node)
            figure = plt.figure()
            plt.axis('off')
            axes = figure.gca()
            board = np.ma.masked_where(board == 0, board)  # For some reason need to mask data to override color
            cmap = plt.cm.get_cmap('gist_rainbow')
            cmap.set_bad(color='gray')  # Overrides the color of 0
            image = axes.imshow(board, interpolation='nearest', cmap=cmap)

            plt.pause(0.1)
        return image

    def draw(self, node):
        if True:
            board = self.visualize(node)
            board = np.ma.masked_where(board == 0, board)
            self.image.set_data(board)
            plt.pause(0.5)  # plt needs to own the main loop which time.sleep does not do, also handles drawing

    def visualize(self, node):
        state = node.state
        board = np.zeros((6, 6))
        i = 1
        for car in state:
            orientation, x_min, y_min, size = car
            if orientation:
                x_max = x_min + 1
                y_max = y_min + size

            else:
                x_max = x_min + size
                y_max = y_min + 1

            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    board[y, x] = i

            i += 1

        return board

    def show_solution(self, node):
        solution = list()
        solution.append(node)
        while node.parent:
            node = node.parent
            solution.append(node)

        print("Path length: ", len(solution))
        if True:
            for node in solution[::-1]:
                print node.printBoard()
                self.draw(node, 2)


def run():
    filename = "Scenarios/expert-2.txt"
    state = loadBoard(filename)
    x= aStar.aStar(State(state))
    g = GUI(x)
    g.show_solution(x)
    #GUI.visualize(x)
    #GUI.show_solution(GUI(x))
    #fig = plt.figure(figsize=[8, 8])
    #plt.show()

    '''
    a = State(state)
    c = a.findLegalMoves()
    for i in c:
        print i.state
    d = c[0].findLegalMoves()
    print "-----"
    for i in d:
        print i.state
    print d[0].state
    printBoard(d[0].board)
    
    '''
run()
