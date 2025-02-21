class Unit:

    __factors = dict(
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
        self.factor = self.__factors[name]


class Units:

    def __init__(self, *, force='kN', moment='kNm', dimensions='mm', stress='MPa'):
        self.force = Unit(force)
        self.moment = Unit(moment)
        self.dimensions = Unit(dimensions)
        self.stress = Unit(stress)
