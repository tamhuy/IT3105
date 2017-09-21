import aStar
import GUI


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
            board[line[1]][line[2]] = state.index(line)
            for i in range(line[3]):
                if line[0] == 0:
                    board[line[1] + i][line[2]] = state.index(line)
                else:
                    board[line[1]][line[2] + i] = state.index(line)
        self.board = board

    def heuristic(self):
        h = 6 - (self.state[0][1] + self.state[0][3])
        h1 = 0
        if self.state[0][1]+self.state[0][3]-1 != 5:
            for i in range(h):
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
            if car[0] == 0:
                if self.board[car[1] - 1][car[2]] == '.' and car[1] != 0:  # Check to see if the car can move to the left
                    tempState = self.state[:]
                    tempState[self.state.index(car)] = [car[0], car[1] - 1, car[2], car[3]]
                    validStates.append(State(tempState))

                if car[1] + car[3] < 6:
                    if self.board[(car[1] + car[3])][car[2]] == '.':  # Check to see if the car can move to the right
                        tempState = self.state[:]
                        tempState[self.state.index(car)] = [car[0], car[1] + 1, car[2], car[3]]
                        validStates.append(State(tempState))

            else:
                if self.board[car[1]][car[2] - 1] == '.' and car[2] != 0:  # check to see if the car can move up
                    tempState = self.state[:]
                    tempState[self.state.index(car)] = [car[0], car[1], car[2] - 1, car[3]]
                    validStates.append(State(tempState))
                if car[2] + car[3] < 6:
                    if self.board[car[1]][car[2] + car[3]] == '.':  # check to see if the car can move down
                        tempState = self.state[:]
                        tempState[self.state.index(car)] = [car[0], car[1], car[2] + 1, car[3]]
                        validStates.append(State(tempState))
        return validStates


def loadBoard(filename):  # Function to read from file
    f = open(filename, 'r')
    board = [['.' for _ in range(6)] for _ in range(6)]
    state = []
    for line in f:
        state.append([int(s) for s in line.split(',')])

    f.close()
    return state


def run():
    filename = "Scenarios/expert-2.txt"
    state = loadBoard(filename)
    x = aStar.aStar(State(state))
    g = GUI.GUI(x)
    g.show_solution(x)


run()
