from toad.settings import SchemaDict

SCHEMA: list[SchemaDict] = [
    {
        "key": "ui",
        "title": "User interface settings",
        "help": "The following settings allow you to customize the look and feel of the User Interface.",
        "type": "object",
        "fields": [
            {
                "key": "column",
                "title": "Enable column?",
                "help": "Enable for a fixed column size. Disable to use the full screen width.",
                "type": "boolean",
                "default": True,
            },
            {
                "key": "column-width",
                "title": "Width of the column",
                "help": "Width of the column if enabled.",
                "type": "integer",
                "default": 100,
                "validate": [{"type": "minimum", "value": 40}],
            },
            {
                "key": "theme",
                "title": "Theme",
                "help": "One of the builtin Textual themes.",
                "type": "choices",
                "default": "dracula",
                "validate": [
                    {
                        "type": "choices",
                        "choices": [
                            "textual-dark",
                            "textual-light",
                            "nord",
                            "gruvbox",
                            "catppuccin-mocha",
                            "dracula",
                            "tokyo-night",
                            "monokai",
                            "flexoki",
                            "catppuccin-late",
                            "solarized-light",
                        ],
                    }
                ],
            },
        ],
    },
    {
        "key": "user",
        "title": "User information",
        "help": "Your details.",
        "type": "object",
        "fields": [
            {
                "key": "name",
                "title": "Your name",
                "type": "string",
                "default": "$USER",
            },
            {
                "key": "email",
                "title": "Your email",
                "type": "string",
                "validate": [{"type": "is_email"}],
                "default": "",
            },
        ],
    },
    {
        "key": "accounts",
        "title": "User accounts",
        "help": "Account details here",
        "type": "object",
        "fields": [
            {
                "key": "anthropic",
                "type": "object",
                "title": "Anthropic account",
                "help": "Instructions how to get an API Key",
                "fields": [
                    {
                        "key": "apikey",
                        "help": "Your API Key goes here",
                        "title": "API Key",
                        "type": "string",
                        "default": "$ANTHROPIC_API_KEY",
                    }
                ],
            },
            {
                "key": "openai",
                "type": "object",
                "title": "OpenAI account",
                "help": "Instructions how to get an OpenAPI API key",
                "fields": [
                    {
                        "key": "apikey",
                        "help": "Your API key goes here",
                        "title": "API Key",
                        "type": "string",
                        "default": "$OPENAI_API_KEY",
                    }
                ],
            },
        ],
    },
]
