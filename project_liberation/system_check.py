from typing import Any

from django.conf import settings
from django.core.checks import Error
from django.core.checks import register

GOOGLE_API_KEYS_ERRORS = {
    "empty": Error(
        "GOOGLE_API_KEY is not declared in settings!",
        hint="Declare GOOGLE_API_KEY attribute in your local settings file.",
    ),
    "type": Error("GOOGLE_API_KEY must be declared in string type!"),
    "length": Error("GOOGLE_API_KEY is of wrong length!"),
}


@register()
def check_google_api_key(app_configs: Any, **kwargs: Any) -> list:  # pylint: disable=unused-argument
    if not hasattr(settings, "GOOGLE_API_KEY"):
        return [GOOGLE_API_KEYS_ERRORS["empty"]]

    if not isinstance(settings.GOOGLE_API_KEY, str):
        return [GOOGLE_API_KEYS_ERRORS["type"]]

    if len(settings.GOOGLE_API_KEY) != 39:
        return [GOOGLE_API_KEYS_ERRORS["length"]]

    return []
