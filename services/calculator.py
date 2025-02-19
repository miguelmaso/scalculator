import numpy as np

class Material:
     
     def stress(self, strain):
          return 0

class Steel(Material):

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

class Section:
    
    __nc = 50

    def __init__(self, b: float, h: float, As: float, As1: float, covering: float):
        self.b = b
        self.h = h
        self.As = As
        self.As1 = As1
        self.covering = covering
        self.concrete = Concrete(3e7)
        self.steel = Steel(5e8)

    @property
    def d(self):
        return self.h - self.covering

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
        epsilon_c = Section.__epsilon(self._z_c, axial, rotation)
        sigma_c = np.array([self.concrete.stress(e) for e in epsilon_c])
        sigma_s = self.steel.stress(Section.__epsilon(self._z_As, axial, rotation))
        sigma_s1 = self.steel.stress(Section.__epsilon(self._z_As1, axial, rotation))
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
        return Section.__epsilon(self._z_c, axial, r)

    def stress_c(self, axial: float):
        strain = self.strain(axial)
        return np.array([self.concrete.stress(e) for e in strain])




class unit:

    factors = dict(
        N = 1,
        kN = 1e-3,
        Nm = 1,
        kNm = 1e-3,
        mm = 1e3,
        cm = 1e-2,
        m = 1,
        Pa = 1,
        kPa = 1e-3,
        MPa = 1e-6
    )

    def __init__(self, name: str):
        self.name = name
        self.factor = self.factors[name]


class units:

    def __init__(self, *, force='kN', moment='kNm', dimensions='mm', stress='MPa'):
        self.force = unit(force)
        self.moment = unit(moment)
        self.dimensions = unit(dimensions)
        self.stress = unit(stress)


uts = units(
    force = 'kN',
    moment = 'kNm',
    dimensions = 'mm'
)



s = Section(0.4, 0.5, 0.003, 0, 0.04)
ax = np.linspace(-s.concrete.e1, s.concrete.e1)
f = np.array([s.forces(a) for a in ax])
N, M = zip(*f)
N = np.array(N)
M = np.array(M)


import plotly.graph_objects as go

layout = go.Layout(
    xaxis = dict(
        minallowed = 0,
        title = f'N ({uts.force.name})',
        fixedrange = True
    ),
    yaxis = dict(
        minallowed = 0,
        title = f'M ({uts.moment.name})',
        fixedrange = True
    )
)
fig = go.Figure(
    data = go.Scatter(x=uts.force.factor*N, y=uts.moment.factor*M),
    layout = layout
)



zero_crossing = np.where(np.diff(np.sign(N)))[0][0]
a0 = ax[zero_crossing]

strain = s.strain(a0)
stresses_c = s.stress_c(a0)
z = s._z_c
stresses_c = np.append(stresses_c, 0)
z_c = np.append(z, z[-1])
xrange_2 = [strain[0] * 1.05, strain[-1] * 1.05]
xrange_1 = [strain[0] / strain[-1] * max(stresses_c) * 1.05, max(stresses_c) * 1.05]

section_layout = go.Layout(
    xaxis = dict(
        range = xrange_1,
        fixedrange = True,
        visible = False
    ),
    xaxis2 = go.layout.XAxis(
        overlaying = 'x',
        range = xrange_2,
        fixedrange = True,
        visible = False
    ),
    yaxis = dict(
        fixedrange = True
    )
)
fig2 = go.Figure(layout=section_layout)
fig2.add_trace(go.Scatter(x=stresses_c, y=z_c, fill='toself'))
fig2.add_trace(go.Scatter(x=strain, y=z, xaxis='x2'))


fig.show()
fig2.show()

