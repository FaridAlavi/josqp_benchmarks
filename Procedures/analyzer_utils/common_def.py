from enum import Enum

class Sol_Status(Enum):
    SOLVED      = 1
    INFEASIBLE  = 2
    NOT_SOLVED  = 3
    SUBOPTIMAL  = 4

class File_Status(Enum):
    FOUND     = 1
    NOT_FOUND = 2
