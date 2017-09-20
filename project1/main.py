import aStar
import module1


class Node:
    f = float("inf")
    g = None
    h = None
    parent = None
    children = []
    state = []

    def __init__(self, state):  # Initialize a node with coordinates, type of character and weight
        self.state = state

board, state = module1.loadBoard("Scenarios/easy-3.txt")

