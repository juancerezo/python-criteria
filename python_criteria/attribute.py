# pyright: reportAttributeAccessIssue=false, reportIncompatibleMethodOverride=false
from typing import Any, Generic, Type, TypeVar, TypeVarTuple, overload

from .clauses import Eq, Ge, Gt, In, Le, Like, Lt, Ne, NotLike

_T_co = TypeVar("_T_co", bound=Any, covariant=True)
_T_tuple = TypeVarTuple("_T_tuple")


class Attribute(Generic[_T_co, *_T_tuple]):
    parent_class: Type[Any]
    type: tuple[Type]
    name: str
    private_name: str
    value: "Attribute[_T_co, *_T_tuple]" | _T_co
    constraints: tuple[Any]

    def __init__(self, _cls, _field, _type, _value, _constraints) -> None:
        self.parent_class = _cls
        self.name = _field
        self.private_name = "__" + _field
        self.type = _type
        self.value = _value
        self.constraints = _constraints

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = "__" + name

    @overload
    def __get__(self, obj: None, objcls) -> "Attribute[_T_co, *_T_tuple]": ...

    @overload
    def __get__(self, obj, objcls) -> _T_co: ...

    def __get__(self, obj, objcls):
        if obj is None:
            return self

        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

    def __hash__(self) -> int:
        return hash((self.parent_class, self.name))

    def __repr__(self) -> str:
        return f"{self.parent_class.__name__}.{self.name}[{self.type[0].__name__}]"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return Eq(self, other)

    def __ne__(self, other):
        return Ne(self, other)

    def __lt__(self, other):
        return Lt(self, other)

    def __le__(self, other):
        return Le(self, other)

    def __gt__(self, other):
        return Gt(self, other)

    def __ge__(self, other):
        return Ge(self, other)

    def __contains__(self, other):
        return In(self, other)

    def like(self, other):
        return Like(self, other)

    def not_like(self, other):
        return NotLike(self, other)
