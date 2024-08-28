from dataclasses import dataclass
from typing import Any, Generic, TypeVar, TypeVarTuple, get_type_hints

from .attribute import Attribute
from .entity import BaseEntity

_T_co = TypeVar("_T_co", bound=Any, covariant=True)
_T_tuple = TypeVarTuple("_T_tuple")


class _BaseConstraints(Generic[_T_co, *_T_tuple]): ...


@dataclass
class AttributeConstraints(_BaseConstraints[Any]):
    searcheable: bool | None = None

    @staticmethod
    def get_searcheable_attributes(entity: type[BaseEntity]) -> tuple[Attribute[Any], ...]:
        attributes = get_type_hints(entity)
        searcheable_attrs: list[Attribute[Any]] = []
        for attr_name in attributes:
            attr: Attribute[Any] = getattr(entity, attr_name)
            for constraint in attr.constraints:
                if not isinstance(constraint, AttributeConstraints):
                    continue

                if constraint.searcheable:
                    searcheable_attrs.append(attr)

        return tuple(searcheable_attrs)
