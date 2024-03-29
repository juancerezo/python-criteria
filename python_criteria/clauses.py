from typing import Any


class BooleanClause:
    field: Any
    value: Any

    def __init__(self, field, value):
        super().__init__()
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
        super().__init__()
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
