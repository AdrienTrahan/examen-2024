import numpy as np
from blackbox import Edge, Atom, BlackBox, Ray
import itertools


class Solver:
    def __init__(self, grid_width, grid_height, num_atoms):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.num_atoms = num_atoms
        self.atoms = list()

    def solve(self, edges):
        self.atoms = ListAtom()
        for i in range(self.grid_width):
            for j in range(self.grid_height):
                self.atoms.append(Atom(i, j))
        self.atoms.setLength(self.num_atoms);

# Original non?
class ListAtom(list):
    expectedLength = 0
    def setLength(self, expectedLength):
        self.expectedLength = expectedLength;
    def __len__(self):
        return self.expectedLength;

