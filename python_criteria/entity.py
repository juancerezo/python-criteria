from typing import Any, dataclass_transform

from .filter import FilterableAttribute, Value

type AnnotatedObject = Any


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
    def __init__(self, /, **kwargs: Any) -> None:
        for name, _type in self.__annotations__.items():  # pylint: disable=no-member
            in_arguments = name in kwargs
            setted_by_default = getattr(self, name).value is not None

            if not in_arguments and not setted_by_default:
                raise ValueError(
                    f"{self.__class__.__name__} constructor key argument '{name}' is missing."
                )

            if not in_arguments and setted_by_default:
                value = getattr(self, name).value.content
                setattr(self, name, value)

            else:
                setattr(self, name, kwargs[name])

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

        for name, _ in _object.__annotations__.items():
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
