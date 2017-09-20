import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

class GUI(ABC):
	def	__init__(self, node):
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
		return image  # Don't need to return the figure anymore as it won't be called

	def draw(self, node, speed):
		if GUI:
			board = self.visualize(node)
			board = np.ma.masked_where(board == 0, board)
			self.image.set_data(board)
			plt.pause(1 / speed)  # plt needs to own the main loop which time.sleep does not do, also handles drawing

	@abstractmethod
	def visualize(self, node):
		pass