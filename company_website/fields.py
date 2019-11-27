import enum


@enum.unique
class ChoiceEnum(enum.Enum):
    """
    Subclass of native python Enum class which can be used in Django models.
    """

    @classmethod
    def choices(cls) -> tuple:
        return tuple((x.name, x.value) for x in cls)
