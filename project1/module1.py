import aStar


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
        h = 5 - self.state[0][1] + self.state[0][3] - 1
        return h

    def isSolution(self):
        if self.state[0][1] == 5 and self.state[0][2] == 2:
            return True

    def findLegalMoves(self):
        validStates = []
        for car in self.state:
            #print "car ", self.state.index(car)
            if car[0] == 0:
                if self.board[car[1] - 1][car[2]] == '.' and car[1] != 0: # Check to see if the car can move to the left
                    #print "valid"
                    tempState = self.state[:]
                    tempState[self.state.index(car)] = [car[0], car[1] - 1, car[2], car[3]]
                    #print tempState
                    validStates.append(State(tempState))
                    #validMove.append([car[0], car[1] - 1, car[2], car[3]])

                if car[1]+car[3] < 6:
                    if self.board[(car[1] + car[3])][car[2]] == '.': # Check to see if the car can move to the right
                        #print "valid"
                        tempState = self.state[:]
                        tempState[self.state.index(car)] = [car[0], car[1] + 1, car[2], car[3]]
                        validStates.append(State(tempState))

            else:
                if self.board[car[1]][car[2] -1] == '.' and car[2] != 0: # check to see if the car can move up
                    #print "valid"
                    tempState = self.state[:]
                    tempState[self.state.index(car)] = [car[0], car[1] , car[2]-1, car[3]]
                    validStates.append(State(tempState))
                if car[2] + car[3] < 6:
                    if self.board[car[1]][car[2] + car[3]] == '.': # check to see if the car can move up
                        #print "valid"
                        tempState = self.state[:]
                        tempState[self.state.index(car)] = [car[0], car[1] , car[2]+1, car[3]]
                        validStates.append(State(tempState))
        '''
        print "0", validStates[0]
        print "1", validStates[1]
        print "2", validStates[2]
        
        '''
        #for i in validStates:
        #    print i.state
        #print validStates[0].state
        return validStates

def loadBoard(filename): #Function to read from file
    f = open(filename, 'r')
    board = [['.' for _ in range(6)] for _ in range(6)]
    state = []
    for line in f:
        state.append([int(s) for s in line.split(',')])

    #print state

    #print board
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




#The A* algorithm is based on the sudo code provided in the "Supplement - Essentials of the AStas Algorithm.pdf" included with the assignment
def aStar(state): #Method for the A* algorithm
    closed, open = [], [] #Initialize open and closed as two lists
    state.g = 0 #Sets the g, h and f values for the starting node
    state.h = state.heuristic()
    state.f = state.g + state.h
    open.append(state) #Adds the starting node to the open list

    while True: #Agenda loop
        if len(open) == 0:# If the goal cannot be reached, return fail
            return False
        x = open.pop() #take the top element of the open stack and place it in the closed stack
        print "----"
        printBoard(x.board)
        #print x.state
        closed.append(x)
        #print x.location #used to see which nodes the algorithm visits
        #print x.f #Used to see the f distance for the current node
        if state.isSolution():# if you have arrived at the end position then end
            return open, closed
        children = state.findLegalMoves()
        print "childre: "
        print children

        #For each successors to the current node
        for i in children:
            print i.state
            if any(i.state == x.state for x in open) or any(i.state == x.state for x in closed):
                continue
            x.children.append(i) #Add the children to the current node

            if i not in open and i not in closed: #The following lines are used to attach the child to the parent and evaluate if the current f distance is shorter or if there is a shorter one
                print "add open"
                attachAndEval(i, x)
                open.append(i)
            elif x.g + i.w < i.g:
                attachAndEval(i, x)
        # Lambda function to sort the open list
        open.sort(key=lambda q: q.f, reverse = True)


def attachAndEval(node, parent):
    node.parent = parent
    node.g = parent.g + 1
    node.h = node.heuristic()
    node.f = node.g + node.h


def propagate(P):
    for c in P.children:
        if P.g + c.w < c.g:
            c.parent = P
            c.g = g
            c.f = c.g + c.h
            propagate(c)





def run():
    filename = "module1/Scenarios/easy-3.txt"
    state = loadBoard(filename)
    #printBoard(board)
    #findLegalMoves(board,state)

    print aStar(State(state))
    #aStar(State([[0, 1, 2, 2], [0, 0, 4, 3], [0, 3, 4, 2], [0, 4, 1, 2], [1, 2, 0, 2], [1, 4, 2, 2]]))
    ###b = State([[0, 1, 2, 2], [0, 0, 4, 3], [0, 3, 4, 2], [0, 4, 1, 2], [1, 2, 0, 2], [1, 4, 2, 2]])
    #print printBoard(b.board)

run()