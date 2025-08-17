from dataclasses import dataclass

from textual.message import Message


class WorkStarted(Message):
    """Work has started."""


class WorkFinished(Message):
    """Work has finished."""


@dataclass
class UserInputSubmitted(Message):
    body: str
    shell: bool = False
