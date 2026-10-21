"""Cell Class"""
import random

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as pat

class Cell:
    """Class for a cell"""

    def __init__(self, position = [0,0], radius=0.1, color=[1,0,0,0.5]):
        """Make a new cell"""
        self.position = np.array(position)
        self.radius = radius
        self.color = color
     
    def show(self):
        """Visualize as a circule"""
        c = plt.Circle(self.position,self.radius,color=self.color)
        plt.gca().add_patch(c)
        plt.axis('equal')


class gCell(Cell):
    """Class of growing cell based on Cell class"""
    
    def grow(self, scale=2):
        """Grow the area of the cell"""
        self.radius *= np.sqrt(scale)
        
    def duplicate(self):
        """Make a copy with a random shift"""
        c = gCell(self.position+np.random.randn(2)*self.radius, self.radius, self.color)
        return c

class dCell(gCell):
    """Class of dividing cell based on Cell class"""

    def divide(self):
        """Divide next to each other"""
        theta = np.random.rand()*2*np.pi
        x_shift = np.cos(theta)*self.radius*2
        y_shift = np.sin(theta)*self.radius*2
        c = dCell(self.position + [x_shift, y_shift], self.radius, self.color)
        return c

class Culture():
    """Class for a cell culture"""

    def __init__(self, n=10, position=None, radius=0.1, color=None):
        """Make a cell culture with n cells"""
        self.number = n  # nuber of cells
        if position == None:  # random position if not specified
            position = np.random.rand(n,2)
        if color == None:  # random colors if not specified
            color = np.random.rand(n,4)
        self.cells = [dCell(position[i],radius=radius,color=color[i]) for i in range(n)]

    def show(self):
        """Visualize as circles"""
        for c in self.cells:
            c.show()

        
    def duplicate(self):
        """Make a copy of each cell"""
        child = [c.duplicate() for c in self.cells]
        self.cells += child
        self.number *= 2

    def divide(self):
        """Divide each cell"""
        child = [c.divide() for c in self.cells]
        self.cells += child
        self.number *= 2

    def move(self, max_iter=1000, tol=1e-9, scale=(1,3)):
        """Move cells apart until there is no overlap, or max_iter is reached."""
        n = len(self.cells)

        for _ in range(max_iter):
            moved = False

            for i in range(n):
                for j in range(i + 1, n):
                    c1 = self.cells[i]
                    c2 = self.cells[j]

                    delta = c1.position - c2.position
                    d = np.linalg.norm(delta)
                    min_distance = c1.radius + c2.radius
                    if scale is not None:
                        min_distance *= random.uniform(*scale)
                    if d < min_distance - tol:
                        if d < tol:
                            # Centers coincide: choose an arbitrary direction
                            direction = np.array([1.0, 0.0])
                        else:
                            direction = delta / d

                        shift = direction * (min_distance - d) / 2
                        c1.position += shift
                        c2.position -= shift
                        moved = True

            if not moved:
                return True  # All pairs are separated

        return False  # Iteration limit reached