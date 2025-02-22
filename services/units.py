class Unit:

    __factors = dict(
        N = 1,
        kN = 1e3,
        Nm = 1,
        kNm = 1e3,
        mm = 1e-3,
        cm = 1e-2,
        m = 1,
        Pa = 1,
        kPa = 1e3,
        MPa = 1e6
    )

    def __init__(self, name: str):
        self.name = name
        self.to_si = self.__factors[name]
        self.from_si = 1 / self.to_si


class Units:

    def __init__(self, *, force='kN', moment='kNm', dimensions='mm', stress='MPa'):
        self.force = Unit(force)
        self.moment = Unit(moment)
        self.dimensions = Unit(dimensions)
        self.stress = Unit(stress)
