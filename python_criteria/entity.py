from collections import ChainMap
from typing import Annotated, Any, dataclass_transform, get_args, get_origin

from .attribute import Attribute

type AnnotatedObject = Any


@dataclass_transform(kw_only_default=True)
class EntityBuilder(type):
    def __init__(cls, name, bases, clsdict) -> None:
        if bases:
            for _field, _type in cls.__annotations__.items():
                value = None
                if hasattr(cls, _field):
                    value = getattr(cls, _field)

                _constraints = []
                _origin_type = get_origin(_type)
                if _origin_type is Annotated:
                    _annotated_types = get_args(_type)
                    _type_args = get_args(_annotated_types[0])
                    _constraints = _annotated_types[1:]

                elif _origin_type is Attribute:
                    _type_args = get_args(_type)

                else:
                    raise TypeError(
                        f"Invalid attribute type. {cls.__name__}.{_field} should be typed as Annotated[Attribute[...], ...] or Attribute[...]"
                    )

                setattr(cls, _field, Attribute(cls, _field, _type_args, value, _constraints))  # type: ignore

        super(EntityBuilder, cls).__init__(name, bases, clsdict)


class BaseEntity(metaclass=EntityBuilder):
    def __init__(self, /, **kwargs: Any) -> None:
        for name, _type in self.__annotations__.items():  # pylint: disable=no-member
            in_arguments = name in kwargs

            if not in_arguments:
                raise ValueError(f"{self.__class__.__name__} constructor key argument '{name}' is missing.")

            else:
                setattr(self, name, kwargs[name])

    def __getattribute__(self, name: str) -> Attribute[Any]:
        return super().__getattribute__(name)

    @classmethod
    def _to_dict(
        cls,
        _object: Any,
        exclude: set[str] | None = None,
        include: set[str] | None = None,
    ) -> dict[str, Any]:
        if exclude is None:
            exclude = set()

        if include is None:
            include = set()

        result: dict[str, Any] = {}

        annotations = ChainMap(
            *(c.__annotations__ for c in _object.__class__.__mro__ if "__annotations__" in c.__dict__)
        )
        for name, _ in annotations.items():
            if name in exclude:
                continue

            if include and name not in include:
                continue

            value = getattr(_object, name)

            if isinstance(value, _object.__class__):
                prefix = f"{name}."
                sub_exclude = set()
                sub_include = set()

                for e in exclude:
                    if not e.startswith(prefix):
                        continue
                    sub_exclude.add(e.removeprefix(prefix))

                for i in include:
                    if not i.startswith(prefix):
                        continue
                    sub_include.add(i.removeprefix(prefix))

                value = cls._to_dict(value, sub_exclude, sub_include)

            result[name] = value

        return result

    @classmethod
    def load(
        cls,
        _object: AnnotatedObject,
        exclude: set[str] | None = None,
        include: set[str] | None = None,
    ):
        return cls(**cls._to_dict(_object, exclude, include))

    def dump(
        self,
        exclude: set[str] | None = None,
        include: set[str] | None = None,
    ) -> dict[str, Any]:
        return self._to_dict(self, exclude, include)
