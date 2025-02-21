import numpy as np

class Material:

    def stress(self, strain):
        raise NotImplementedError()

class ReinforcingSteel(Material):

    def __init__(self, fy: float):
        self.fy = fy
        self.E = 2.1e11
        self.e1 = 2 * self.fy / self.E

    def stress(self, strain: float):
        elastic = self.E * strain
        return min(self.fy, elastic)

class Concrete(Material):

    def __init__(self, fc: float):
        self.fc = fc
        self.E = 5e6 * np.sqrt(fc)
        self.e1 = 0.0032

    def stress(self, strain: float):
        elastic = self.E * strain
        return min(self.fc, max(0, elastic))
