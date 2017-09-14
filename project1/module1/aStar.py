#The A* algorithm is based on the sudo code provided in the "Supplement - Essentials of the AStas Algorithm.pdf" included with the assignment
def aStar(state): #Method for the A* algorithm
    print "A*"
    closed, open = [], [] #Initialize open and closed as two lists
    state.g = 0 #Sets the g, h and f values for the starting node
    state.h = state.heuristic()
    state.f = state.g + state.h
    open.append(state) #Adds the starting node to the open list

    while True: #Agenda loop
        #print "hei"
        if len(open) == 0:# If the goal cannot be reached, return fail
            return False
        x = open.pop() #take the top element of the open stack and place it in the closed stack
        #print "----"
        #printBoard(x.board)
        #print x.state
        closed.append(x)
        #print x.location #used to see which nodes the algorithm visits
        #print x.f #Used to see the f distance for the current node
        if x.isSolution():# if you have arrived at the end position then end
            print len(open) + len(closed)
            moves = 0
            while x.parent != None:
                moves += 1
                print "---"
                x.printBoard()
                x = x.parent
            print moves
            return open, closed
        children = x.findLegalMoves()
        #print "state: ", x.state
        #print x.printBoard()
        #print "children: "
        #print children

        #For each successors to the current node
        for i in children:
            #print i.state
            if any(i.state == x.state for x in open) or any(i.state == x.state for x in closed):
                continue
            x.children.append(i) #Add the children to the current node

            #if i not in open and i not in closed: #The following lines are used to attach the child to the parent and evaluate if the current f distance is shorter or if there is a shorter one
            if not (any(i.state == x.state for x in open) and any(i.state == x.state for x in closed)):
                #print "add open"
                attachAndEval(i, x)
                open.append(i)
            elif x.g + 1 < i.g:
                print "propagate"
                attachAndEval(i, x)
                if i in closed:
                   propagate(i)
        # Lambda function to sort the open list
        open.sort(key=lambda q: q.f, reverse = True)


def attachAndEval(node, parent):
    node.parent = parent
    node.g = parent.g + 1
    node.h = node.heuristic()
    node.f = node.g + node.h


def propagate(P):
    for c in P.children:
        if P.g + 1 < c.g:
            c.parent = P
            c.g = P.g + 1
            c.f = c.g + c.h
            propagate(c)

