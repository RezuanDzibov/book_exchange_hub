import enum


class ConditionEnum(enum.Enum):
    GOOD = "good"
    WELL = "well"
    NORMAL = "normal"
    BAD = "bad"
    VERY_BAD = "very_bad"


class BookExchangeStatus(enum.Enum):
    CREATED = "created"
    PROCESSING = "processing"
    VALIDATED = "validated"
    SUCCESS = "success"
    FAILED = "failed"
