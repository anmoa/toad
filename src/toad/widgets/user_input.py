from textual.app import ComposeResult
from textual import containers
from textual.widgets import Markdown

from toad.widgets.non_selectable_label import NonSelectableLabel


class UserInput(containers.HorizontalGroup):
    def __init__(self, content: str) -> None:
        super().__init__()
        self.content = content

    def compose(self) -> ComposeResult:
        yield NonSelectableLabel("❯", id="prompt")
        yield Markdown(self.content, id="content")
