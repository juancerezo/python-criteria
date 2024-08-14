# pyright: reportAttributeAccessIssue=false, reportIncompatibleMethodOverride=false
from typing import Any, Generic, Type, TypeVar, overload

from .clauses import (
    BooleanClause,
    BooleanClauseList,
    Eq,
    Ge,
    Gt,
    In,
    Le,
    Like,
    Lt,
    Ne,
    NotLike,
)

type ClauseType = BooleanClause | BooleanClauseList
_T_co = TypeVar("_T_co", bound=Any, covariant=True)


class Filter:
    __clauses: ClauseType | None

    def __init__(self, clause: ClauseType | None = None) -> None:
        self.__clauses = clause

    def __and__(self, clause: ClauseType):
        if self.__clauses is None:
            self.__clauses = clause

        self.__clauses = self.__clauses & clause

        return self

    def __or__(self, clause: ClauseType):
        if self.__clauses is None:
            self.__clauses = clause

        self.__clauses = self.__clauses | clause

        return self

    @property
    def clause(self):
        return self.__clauses


class _AttributeBase(Generic[_T_co]): ...


class Attribute(_AttributeBase[_T_co]):
    parent_class: Type
    type: tuple[Type]
    name: str
    value: "Attribute[_T_co]" | _T_co

    def __init__(self, _cls, _field, _type, _value) -> None:
        self.parent_class = _cls
        self.name = _field
        self.type = _type
        self.value = _value

    @overload
    def __get__(self, instance: None, owner) -> "Attribute[_T_co]": ...

    @overload
    def __get__(self, instance, owner) -> _T_co: ...

    def __get__(self, instance, owner) -> "Attribute[_T_co]" | _T_co:
        if instance is None:
            return self

        return self.value

    def __set__(self, instance, value) -> None:
        self.value = value

    def __hash__(self) -> int:
        return hash((self.parent_class, self.name))

    def __repr__(self) -> str:
        return f"{self.parent_class.__name__}.{self.name}[{self.type.__name__}]"

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
