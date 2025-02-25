import numpy as np
from services.materials import Concrete, ReinforcingSteel
from services.codes import UNE_EN

class Section:

    @property
    def area(self):
        raise NotImplementedError()

class ConcreteSection(Section):
    
    __nc = 50

    def __init__(self, b: float, h: float, As: float, As1: float, covering: float):
        self.b = b
        self.h = h
        self.As = As
        self.As1 = As1
        self.covering = covering
        self.concrete = Concrete(3e7)
        self.steel = ReinforcingSteel(5e8)

    def minimum_reinforcement(self, structure):
        ratio = UNE_EN.minimum_reinforcement_ratio(self, structure)
        minimum = self.area * ratio
        perim = 2 * (self.b + self.h)
        return {
            'top' : minimum * self.b / perim,
            'bottom' : minimum * self.b / perim,
            'side' : minimum * self.h / perim
        }

    @property
    def area(self):
        return self.b * self.h

    @property
    def d(self):
        return self.h - self.covering

    @property
    def reduced_moment(self):
        return 0.25 * self.b * self.h**2 * self.concrete.fc

    @property
    def _z_As(self):
        return -0.5 * self.h + self.covering
    
    @property
    def _z_As1(self):
        return 0.5 * self.h - self.covering

    @property
    def _z_c(self):
            return np.linspace(-0.5 * self.h, 0.5 * self.h, self.__nc)
    
    @staticmethod
    def __epsilon(z, axial: float, rotation: float):
        return axial + rotation * z
    
    def __max_rotation(self, axial: float):
        max_r_c = 2 * (self.concrete.e1 - axial) / self.h
        max_r_s = (-self.steel.e1 - axial) / self._z_As
        return min(max_r_c, max_r_s)

    def __forces(self, axial: float, rotation: float):
        epsilon_c = self.__epsilon(self._z_c, axial, rotation)
        sigma_c = np.array([self.concrete.stress(e) for e in epsilon_c])
        sigma_s = self.steel.stress(self.__epsilon(self._z_As, axial, rotation))
        sigma_s1 = self.steel.stress(self.__epsilon(self._z_As1, axial, rotation))
        dz = self.h/(self.__nc-1)
        N = np.trapezoid(sigma_c, dx=dz)
        N += sigma_s * self.As
        N += sigma_s1 * self.As1
        sigma_cz = np.multiply(sigma_c, self._z_c)
        M = np.trapezoid(sigma_cz, dx=dz)
        M += sigma_s * self._z_As * self.As
        M += sigma_s1 * self._z_As1 * self.As1
        return (N, M)
    
    def forces(self, axial: float):
        r = self.__max_rotation(axial)
        return self.__forces(axial, r)

    def strain(self, axial: float):
        r = self.__max_rotation(axial)
        return self.__epsilon(self._z_c, axial, r)

    def stress_c(self, axial: float):
        strain = self.strain(axial)
        return np.array([self.concrete.stress(e) for e in strain])
