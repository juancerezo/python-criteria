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

                setattr(cls, _field, FilterableAttribute(cls, _field, _type, value))

        super(EntityBuilder, cls).__init__(name, bases, clsdict)


class BaseEntity(metaclass=EntityBuilder):
    def __init__(self, /, **data: Any) -> None:
        for name, _type in self.__annotations__.items():  # pylint: disable=no-member
            if not hasattr(self, name):
                raise ValueError(f"'{self.__class__.__name__}.{name}' is missing.")

            setattr(self, name, data[name])
