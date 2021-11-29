from enum import Enum
from typing import Tuple


class Colors(Tuple, Enum):
    BLACK = (41, 41, 41)
    WHITE = (245, 245, 245)
    GARY = (220, 220, 220)
    PATH = (119, 214, 140)
    EXPLORE = (121, 119, 214)
    GOAL = (204, 60, 100)
    START = (255, 153, 0)
