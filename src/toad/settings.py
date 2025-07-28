from __future__ import annotations

from functools import cached_property

from dataclasses import dataclass
from typing import Iterable, Sequence, TypedDict, Required

from toad._loop import loop_last


@dataclass
class Setting:
    """A setting or group of setting."""

    key: str
    title: str
    type: str = "object"
    help: str = ""
    default: object | None = None
    validate: list[dict] | None = None
    children: dict[str, Setting] | None = None


class SchemaDict(TypedDict, total=False):
    """Typing for schema data structure."""

    key: Required[str]
    title: Required[str]
    type: Required[str]
    help: str
    default: object
    fields: list[SchemaDict]
    validate: list[dict]


type SettingsType = dict[str, object]


INPUT_TYPES = {"boolean", "integer", "string", "choices"}


class SettingsError(Exception):
    """Base class for settings related errors."""


class InvalidKey(SettingsError):
    """The key is not in the schema."""


class InvalidValue(SettingsError):
    """The value was not of the expected type."""


def parse_key(key: str) -> Sequence[str]:
    return key.split(".")


def get_setting[ExpectType](
    settings: dict[str, object], key: str, expect_type: type[ExpectType] = object
) -> ExpectType:
    """Get a key from a settings structure.

    Args:
        settings: A settings dictionary.
        key: A dot delimited key, e.g. "ui.column"
        expect_type: The expected type of the value.

    Raises:
        InvalidValue: If the value is not the expected type.
        KeyError: If the key doesn't exist in settings.

    Returns:
        The value matching they key.
    """
    for last, key_component in loop_last(parse_key(key)):
        if last:
            result = settings[key_component]
            if not isinstance(result, expect_type):
                raise InvalidValue(
                    f"Expected {expect_type.__name__} type; found {result!r}"
                )
            return result
        else:
            sub_settings = settings[key_component]
            assert isinstance(sub_settings, dict)
            settings = sub_settings
    raise KeyError(key)


class Schema:
    def __init__(self, schema: list[SchemaDict]) -> None:
        self.schema = schema

    def set_value(self, settings: SettingsType, key: str, value: object) -> None:
        schema = self.schema
        keys = parse_key(key)
        for last, key in loop_last(keys):
            if last:
                settings[key] = value
            if key not in schema:
                raise InvalidKey()
            schema = schema[key]
            assert isinstance(schema, dict)
            if key not in settings:
                settings = settings[key] = {}

    def defaults(self) -> dict[str, object]:
        settings: dict[str, object] = {}

        def set_defaults(schema: list[SchemaDict], settings: dict[str, object]) -> None:
            sub_settings: SettingsType
            for sub_schema in schema:
                key = sub_schema["key"]
                assert isinstance(sub_schema, dict)
                type = sub_schema["type"]

                if type == "object":
                    if fields := sub_schema.get("fields"):
                        sub_settings = settings[key] = {}
                        set_defaults(fields, sub_settings)

                else:
                    if (default := sub_schema.get("default")) is not None:
                        settings[key] = default

        set_defaults(self.schema, settings)
        return settings

    @cached_property
    def keys(self) -> Sequence[str]:
        def get_keys(setting: Setting) -> Iterable[str]:
            if setting.type == "object" and setting.children:
                for child in setting.children.values():
                    yield from get_keys(child)
            else:
                yield setting.key

        keys = [
            key for setting in self.settings_map.values() for key in get_keys(setting)
        ]
        return keys

    @cached_property
    def settings_map(self) -> dict[str, Setting]:
        form_settings: dict[str, Setting] = {}

        def build_settings(
            name: str, schema: SchemaDict, default: object = None
        ) -> Setting:
            schema_type = schema.get("type")
            assert schema_type is not None
            if schema_type == "object":
                return Setting(
                    name,
                    schema["title"],
                    schema_type,
                    help=schema.get("help") or "",
                    default=schema.get("default", default),
                    validate=schema.get("validate"),
                    children={
                        schema["key"]: build_settings(f"{name}.{schema['key']}", schema)
                        for schema in schema.get("fields", [])
                    },
                )
            else:
                return Setting(
                    name,
                    schema["title"],
                    schema_type,
                    help=schema.get("help") or "",
                    default=schema.get("default", default),
                    validate=schema.get("validate"),
                )

        for sub_schema in self.schema:
            form_settings[sub_schema["key"]] = build_settings(
                sub_schema["key"], sub_schema
            )
        return form_settings


class Settings:
    """Stores schema backed settings."""

    def __init__(self, schema: Schema, settings: dict[str, object]) -> None:
        self._schema = schema
        self._settings = settings

    def get[ExpectType](
        self, key: str, expect_type: type[ExpectType] = object
    ) -> ExpectType:
        from os.path import expandvars

        setting = get_setting(self._settings, key, expect_type=expect_type)
        if isinstance(setting, str):
            setting = expandvars(setting)
        return setting


if __name__ == "__main__":
    from rich import print
    from rich.traceback import install

    from toad.settings_schema import SCHEMA

    install(show_locals=True, width=None)

    schema = Schema(SCHEMA)
    settings = schema.defaults
    print(settings)

    print(schema.settings_map)

    print(schema.keys)
