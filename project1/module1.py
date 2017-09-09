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

    #tall = 0 #A number used to increment

    """
    for line in f: #Goes through the txt file one line at a time
        board.append([]) #Elements in each line so it can be a 2-dimensional list
        for x in range(len(line)):
            if line[x] == '#': #Initilizes the walls whit a infinte weight
                board[tall].append(Node(tall, x, line[x], float("inf")))
            elif line[x] == 'w':
                board[tall].append(Node(tall, x, line[x], 100))
            elif line[x] == 'm':
                board[tall].append(Node(tall, x, line[x], 50))
            elif line[x] == 'f':
                board[tall].append(Node(tall, x, line[x], 10))
            elif line[x] == 'g':
                board[tall].append(Node(tall, x, line[x], 5))
            elif line[x] == 'r':
                board[tall].append(Node(tall, x, line[x], 1))
            else: #Initializes the rest of the nodes with weight 1
                board[tall].append(Node(tall, x, line[x], 1))

        del board[tall][-1] #Deletes the '\n'
        tall += 1
    """
    f.close()
    return board

def run():
    filename = "module1/Scenarios/easy-3.txt"
    board = loadBoard(filename)
    print board

run()