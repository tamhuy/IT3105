import GUI

#The A* algorithm is based on the sudo code provided in the "Essentials of the A* Algorithm.pdf" included with the assignment
def aStar(state): #Method for the A* algorithm
    print "A*"
    gui = False
    closed, open = [], [] #Initialize open and closed as two lists
    state.g = 0 #Sets the g, h and f values for the starting node
    state.h = state.heuristic()
    state.f = state.g + state.h
    open.append(state) #Adds the starting node to the open list
    if gui:
        g = GUI.GUI(state)

    while True: #Agenda loop
        if len(open) == 0:# If the goal cannot be reached, return fail
            return False
        x = open.pop() #take the top element of the open stack and place it in the closed stack
        if gui:
            g.draw(x)
        closed.append(x)
        if x.isSolution():# if you have arrived at the end position then end
            print len(open) + len(closed)
            return x
        children = x.findLegalMoves()

        #For each successors to the current node
        for i in children:
            if any(i.state == x.state for x in open) or any(i.state == x.state for x in closed):
                continue
            x.children.append(i) #Add the children to the current node

            #if i not in open and i not in closed: #The following lines are used to attach the child to the parent and evaluate if the current f distance is shorter or if there is a shorter one
            if not (any(i.state == x.state for x in open) and any(i.state == x.state for x in closed)):
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

