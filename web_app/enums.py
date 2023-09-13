import enum


class TypeOfActivity(enum.Enum):
    CALL = "call"
    MEETING = "meeting"
    TASK = "task"


class ActivityStatus(enum.Enum):
    IN_PROGRESS = "in progress"
    COMPLETE = "comlete"
    OVERDUE = "overdue"
