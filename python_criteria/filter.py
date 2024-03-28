# pyright: reportAttributeAccessIssue=false, reportIncompatibleMethodOverride=false
from typing import Any, Type


class Value:
    content: Any

    def __init__(self, content) -> None:
        self.content = content


class FilterableAttribute:
    parent_class: Type
    type: Type
    name: str
    value: Value | None

    def __init__(self, _cls, _field, _type, _value) -> None:
        self.parent_class = _cls
        self.name = _field
        self.type = _type
        self.value = _value

    def __repr__(self) -> str:
        return f"{self.parent_class.__name__}.{self.name}[{self.type.__name__}]"

    def __str__(self):
        return f"{self.parent_class.__name__}.{self.name}"

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

    def in_(self, other):
        return In(self, other)

    def like(self, other):
        return Like(self, other)

    def not_like(self, other):
        return NotLike(self, other)


class BooleanClause:
    field: FilterableAttribute
    value: Any

    def __init__(self, field, value):
        self.field = field
        self.value = value

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __xor__(self, other):
        return Xor(self, other)

    def __invert__(self):
        return Not(self)


class Eq(BooleanClause):
    def __str__(self):
        return f"{self.field} == '{self.value}'"


class Ne(BooleanClause):
    def __str__(self):
        return f"{self.field} != '{self.value}'"


class Lt(BooleanClause):
    def __str__(self):
        return f"{self.field} < '{self.value}'"


class Le(BooleanClause):
    def __str__(self):
        return f"{self.field} <= '{self.value}'"


class Gt(BooleanClause):
    def __str__(self):
        return f"{self.field} > '{self.value}'"


class Ge(BooleanClause):
    def __str__(self):
        return f"{self.field} >= '{self.value}'"


class In(BooleanClause):
    def __str__(self):
        return f"{self.field} in '{self.value}'"


class Like(BooleanClause):
    def __str__(self):
        return f"{self.field} like '{self.value}'"


class NotLike(BooleanClause):
    def __str__(self):
        return f"{self.field} not_like '{self.value}'"


class BooleanClauseList:
    clause_list: tuple["BooleanClauseList", ...]

    def __init__(self, *clause_list):
        self.clause_list = clause_list

    def __and__(self, other):
        return And(self, other)

    def __or__(self, other):
        return Or(self, other)

    def __xor__(self, other):
        return Xor(self, other)

    def __invert__(self):
        return Not(self)


class And(BooleanClauseList):
    def __and__(self, other):
        if isinstance(other, And):
            self.clause_list += other.clause_list
        else:
            self.clause_list += (other,)

        return self

    def __str__(self):
        return " & ".join([str(clause) for clause in self.clause_list])


class Or(BooleanClauseList):
    def __or__(self, other):
        if isinstance(other, Or):
            self.clause_list += other.clause_list
        else:
            self.clause_list += (other,)
        return self

    def __str__(self):
        return " | ".join([str(clause) for clause in self.clause_list])


class Not(BooleanClauseList):
    def __str__(self):
        return f"~ {self.clause_list[0]}"


class Xor(BooleanClauseList):
    def __str__(self):
        return f"{self.clause_list[0]} ^ '{self.clause_list[1]}'"
