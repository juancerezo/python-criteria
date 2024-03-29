from typing import Any

type SQLAlchemyTable = Any

from .clauses import BooleanClause
from .visitor import BaseVisitor


class SQLAlchemyVisitor(BaseVisitor):
    def __init__(self, mapping_object: SQLAlchemyTable) -> None:
        super().__init__(mapping_object)

    def visit_eq(self, comparison: BooleanClause):
        return self._attr(comparison.field) == comparison.value

    def visit_ne(self, comparison: BooleanClause):
        return self._attr(comparison.field) != comparison.value

    def visit_lt(self, comparison: BooleanClause):
        return self._attr(comparison.field) < comparison.value

    def visit_le(self, comparison: BooleanClause):
        return self._attr(comparison.field) <= comparison.value

    def visit_gt(self, comparison: BooleanClause):
        return self._attr(comparison.field) > comparison.value

    def visit_ge(self, comparison: BooleanClause):
        return self._attr(comparison.field) >= comparison.value

    def visit_in(self, comparison: BooleanClause):
        return self._attr(comparison.field).in_(comparison.value)

    def visit_like(self, comparison: BooleanClause):
        return self._attr(comparison.field).ilike(comparison.value, escape="\\")

    def visit_not_like(self, comparison: BooleanClause):
        return self._attr(comparison.field).not_ilike(comparison.value, escape="\\")

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
