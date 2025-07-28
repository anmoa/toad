from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

from textual.app import ComposeResult
from textual import containers
from textual.screen import ModalScreen
from textual.widget import Widget
from textual.widgets import Input, Label, Select, Checkbox, Footer

from toad.settings import Setting

if TYPE_CHECKING:
    from toad.app import ToadApp


class SettingsInput(Input):
    pass


class SettingsScreen(ModalScreen):
    BINDINGS = [("escape", "dismiss", "Dismiss settings")]

    app: ToadApp

    def compose(self) -> ComposeResult:
        schema = self.app.settings_schema

        def schema_to_widget(settings_map: dict[str, Setting]) -> Iterable[Widget]:
            for key, setting in settings_map.items():
                if setting.type == "object":
                    if setting.children is not None:
                        yield Label(setting.title, classes="title")
                        if setting.help:
                            yield Label(setting.help, classes="help")
                        grid = containers.VerticalGroup(
                            *schema_to_widget(setting.children),
                            classes="container",
                        )

                        yield grid
                else:
                    yield Label(setting.title, classes="title")
                    if setting.help:
                        yield Label(setting.help, classes="help")
                    if setting.type == "string":
                        yield SettingsInput(str(setting.default))
                    elif setting.type == "boolean":
                        yield Checkbox()
                    elif setting.type == "integer":
                        yield SettingsInput(str(setting.default), type="integer")
                    elif setting.type == "choices":
                        yield Select.from_values(setting.validate[0]["choices"])

        with containers.VerticalScroll():
            yield from schema_to_widget(schema.settings_map)
        yield Footer()
