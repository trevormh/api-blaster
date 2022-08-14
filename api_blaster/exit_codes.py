from enum import unique, Enum

@unique
class ExitCodes(Enum):
    SUCCESS = 0
    GENERAL_ERROR = 1
    FILE_OR_DIR_NOT_FOUND = 2
    CTL_C = 130
