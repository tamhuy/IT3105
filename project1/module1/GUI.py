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

            plt.pause(0.1)
        return image

    def draw(self, node):
        if True:
            board = self.visualize(node)
            board = np.ma.masked_where(board == 0, board)
            self.image.set_data(board)
            plt.pause(0.1)  # plt needs to own the main loop which time.sleep does not do, also handles drawing

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

        print("Path length: ", len(solution) -1)
        for node in solution[::-1]:
            self.draw(node)