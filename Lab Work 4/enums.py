from enum import Enum, auto

class SideType(Enum):
    RED = auto()
    BLUE = auto()

    def opposite(side):
        if (side == SideType.RED):
            return SideType.BLUE
        elif (side == SideType.BLUE):
            return SideType.RED
        else: raise ValueError()

class CheckerType(Enum):
    NONE = auto()
    RED_REGULAR = auto()
    BLUE_REGULAR = auto()
    RED_QUEEN = auto()
    BLUE_QUEEN = auto()