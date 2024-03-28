from typing import Any

from .filter import BooleanClause, FilterableAttribute
from .visitor import Visitor

type SQLAlchemyTable = Any


class SQLAlchemyVisitor(Visitor):
    def __init__(self, table: SQLAlchemyTable) -> None:
        super().__init__()
        self.table = table

    def __attr(self, field: FilterableAttribute):
        if not hasattr(self.table, field.name):
            raise ValueError(
                f"'{field.name}' is not a valid attribute of '{field.parent_class.__name__}'"
            )

        return getattr(self.table, field.name)

    def visit_eq(self, comparison: BooleanClause):
        return self.__attr(comparison.field) == comparison.value

    def visit_ne(self, comparison: BooleanClause):
        return self.__attr(comparison.field) != comparison.value

    def visit_lt(self, comparison: BooleanClause):
        return self.__attr(comparison.field) < comparison.value

    def visit_le(self, comparison: BooleanClause):
        return self.__attr(comparison.field) <= comparison.value

    def visit_gt(self, comparison: BooleanClause):
        return self.__attr(comparison.field) > comparison.value

    def visit_ge(self, comparison: BooleanClause):
        return self.__attr(comparison.field) >= comparison.value

    def visit_in(self, comparison: BooleanClause):
        return self.__attr(comparison.field).in_(comparison.value)

    def visit_like(self, comparison: BooleanClause):
        return self.__attr(comparison.field).ilike(comparison.value, escape="\\")

    def visit_not_like(self, comparison: BooleanClause):
        return self.__attr(comparison.field).not_ilike(comparison.value, escape="\\")

    def visit_or(self, comparisons: list[Any]):
        _op = comparisons[0]
        for comp in comparisons[1:]:
            _op = _op | comp  #! <--- Caution: do not modify bitwise operator

        return _op

    def visit_and(self, comparisons: list[Any]):
        _op = comparisons[0]
        for comp in comparisons[1:]:
            _op = _op & comp  #! <--- Caution: do not modify bitwise operator
        return _op

    def visit_xor(self, comparisons: list[Any]):
        return (
            comparisons[0] ^ comparisons[1]
        )  #! <--- Caution: do not modify bitwise operator

    def visit_not(self, comparisons: list[Any]):
        return ~comparisons[0]  #! <--- Caution: do not modify bitwise operator
