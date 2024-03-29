from typing import Any

from typing_extensions import dataclass_transform

from .filter import FilterableAttribute, Value


@dataclass_transform(kw_only_default=True)
class EntityBuilder(type):
    def __init__(cls, name, bases, clsdict) -> None:
        if bases:
            for _field, _type in cls.__annotations__.items():
                value = None
                if hasattr(cls, _field):
                    value = Value(getattr(cls, _field))

                setattr(cls, _field, FilterableAttribute(cls, _field, _type, value))  # type: ignore

        super(EntityBuilder, cls).__init__(name, bases, clsdict)


class BaseEntity(metaclass=EntityBuilder):
    def __init__(self, /, **data: Any) -> None:
        for name, _type in self.__annotations__.items():  # pylint: disable=no-member
            in_arguments = hasattr(data, name)
            setted_by_default = getattr(self, name).value is not None

            if not in_arguments and not setted_by_default:
                raise ValueError(
                    f"{self.__class__.__name__} constructor key argument '{name}' is missing."
                )

            elif not in_arguments and setted_by_default:
                value = getattr(self, name).value.content
                setattr(self, name, value)

            else:
                setattr(self, name, data[name])
