from enum import Enum, auto

class StructureTypes(Enum):
    beam = auto()
    slab = auto()
    wall = auto()
    column = auto()

class UNE_EN:
    
    __min_reinf = {
        StructureTypes.beam : 4e-3,
        StructureTypes.column : 4e-3,
        StructureTypes.slab : 4e-3,
        StructureTypes.wall : 4e-3
    }

    @classmethod
    def minimum_reinforcement_ratio(cls, structure: StructureTypes):
        return cls.__min_reinf[structure]
