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

STORAGE_DIRECTORIES_SETTING_NAMES = ["COMPANY_EMPLOYEES_STORAGE", "TESTIMONIAL_PHOTOS_STORAGE"]


def setting_not_declared_error(setting_name: str) -> Error:
    return Error(f"{setting_name} is not declared in settings!")


def setting_not_a_string_error(setting_name: str) -> Error:
    return Error(f"{setting_name} is not a string!")


@register()
def check_google_api_key(app_configs: Any, **kwargs: Any) -> list:  # pylint: disable=unused-argument
    if not hasattr(settings, "GOOGLE_API_KEY"):
        return [GOOGLE_API_KEYS_ERRORS["empty"]]

    if not isinstance(settings.GOOGLE_API_KEY, str):
        return [GOOGLE_API_KEYS_ERRORS["type"]]

    if len(settings.GOOGLE_API_KEY) != 39:
        return [GOOGLE_API_KEYS_ERRORS["length"]]

    return []


@register()
def check_custom_storage_directories(app_configs: Any, **kwargs: Any) -> list:  # pylint: disable=unused-argument
    errors = []
    for setting_name in STORAGE_DIRECTORIES_SETTING_NAMES:
        if not hasattr(settings, setting_name):
            errors.append(setting_not_declared_error(setting_name))

        elif not isinstance(getattr(settings, setting_name), str):
            errors.append(setting_not_a_string_error(setting_name))
    return errors
