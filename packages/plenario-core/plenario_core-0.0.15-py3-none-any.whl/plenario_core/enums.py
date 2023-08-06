from enum import Enum
from typing import List, Tuple


class DjangoEnum(Enum):
    """A base class that provides helpful methods to enums used as fields.
    """

    def __str__(self) -> str:
        return self.value

    @classmethod
    def as_choices(cls) -> List[Tuple[str, str]]:
        return [(attr.value, attr.name) for attr in cls]

    @classmethod
    def has_value(cls, value: str) -> bool:
        return value in [attr.value for attr in cls]

class RefreshRate(DjangoEnum):
    """A control structure for handling ETL cadence.
    """

    Minutes = 'minutes'
    Hours = 'hours'
    Days = 'days'
    Months = 'months'
    Years = 'years'
    Never = 'never'


class EtlState(DjangoEnum):
    """A control structure for handling queryability and state of ETL models.
    """

    New = 'new'
    Approved = 'approved'
    Ready = 'ready'
    Locked = 'locked'
    Erred = 'erred'


class StreamState(DjangoEnum):
    """A control structure for handling queryability and state of stream models.
    """

    New = 'new'
    Approved = 'approved'
    Ready = 'ready'
    Erred = 'erred'
