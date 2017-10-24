"""This module for interaction with graph."""
import matplotlib.pyplot as plt
import numpy as np
import time

from PyQt5 import QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Graph():
    
    def __init__(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.setUp()
    
    def draw(self, x, y):
        """
        Draw graph.

        Parameters:
        -----------
        x : float
            The value of the axis x.
        y : float
            The value of the axis y.
        """
        
        self.hl.set_xdata(np.append(self.hl.get_xdata(), x))
        self.hl.set_ydata(np.append(self.hl.get_ydata(), y))
        self.ax.relim()
        self.ax.autoscale_view(False,True,True)
        self.canvas.draw()
        
    
    def clear(self):
        """Clears graph."""
        self.ax.cla()
        self.setUp()
    
    def setUp(self):
        """Set up graph."""
        self.ax = self.figure.add_subplot(111)
        self.ax.set_autoscale_on(True)
        self.ax.grid()
        self.hl, = self.ax.plot(0)
        self.canvas.draw()

if __name__ == '__main__':
    graph = Graph()