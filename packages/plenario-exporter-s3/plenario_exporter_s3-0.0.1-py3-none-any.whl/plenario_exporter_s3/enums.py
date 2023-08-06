from enum import Enum


class State(Enum):
    New = 'new'
    Processing = 'processing'
    Completed = 'completed'
    Erred = 'erred'

    def __str__(self) -> str:
        return self.value
