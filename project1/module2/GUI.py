import matplotlib.pyplot as plt
import numpy as np


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

            plt.pause(0)
        return image

    def draw(self, node):
        if True:
            board = self.visualize(node)
            board = np.ma.masked_where(board == 0, board)
            self.image.set_data(board)
            plt.pause(10)  # plt needs to own the main loop which time.sleep does not do, also handles drawing

    def visualize(self, node):
        #state = node.state
        board = np.zeros((node.rows, node.columns))
        #print node.domains[node.variables[0]][0][0]
        for i in range(node.rows):
            for j in range(node.columns):
                if node.domains[node.variables[i]][0][j] == True:
                    board[node.rows-1-i, j] = 1
                #print node.domains[node.variables[i]]
        '''
        for i in range(7):
            if i.type == "column":
                break
            print node.domains[i]
            for x in range(7):
                for y in range(6):

                    board[y, x] = 1
        
        '''





        return board

    def show_solution(self, node):
        solution = list()
        solution.append(node)
        while node.parent:
            node = node.parent
            solution.append(node)

        print("Path length: ", len(solution) -1)
        for node in solution[::-1]:
            self.draw(node)