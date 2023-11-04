import enum


class TypeOfActivity(enum.Enum):
    CALL: str = "call"
    MEETING: str = "meeting"
    TASK: str = "task"


class ActivityStatus(enum.Enum):
    IN_PROGRESS: str = "in progress"
    COMPLETE: str = "completed"
    OVERDUE: str = "overdue"


class Roles(enum.Enum):
    HEAD_OF_COMPANY: int = 3
    HEAD_OF_DEPART: int = 2
    MANAGER: int = 1

