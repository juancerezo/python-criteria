from typing import Any

type SQLAlchemyTable = Any

from .clauses import BooleanClause
from .visitor import BaseVisitor


class SQLAlchemyVisitor(BaseVisitor):
    def visit_eq(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field) == comparison.value

    def visit_ne(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field) != comparison.value

    def visit_lt(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field) < comparison.value

    def visit_le(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field) <= comparison.value

    def visit_gt(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field) > comparison.value

    def visit_ge(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field) >= comparison.value

    def visit_in(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field).in_(comparison.value)

    def visit_like(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field).ilike(
            comparison.value, escape="\\"
        )

    def visit_not_like(self, mapping_object: Any, comparison: BooleanClause):
        return self._attr(mapping_object, comparison.field).not_ilike(
            comparison.value, escape="\\"
        )

    def visit_or(self, mapping_object: Any, comparisons: list[Any]):
        _op = comparisons[0]
        for comp in comparisons[1:]:
            _op = _op | comp  #! <--- Caution: do not modify bitwise operator

        return _op

    def visit_and(self, mapping_object: Any, comparisons: list[Any]):
        _op = comparisons[0]
        for comp in comparisons[1:]:
            _op = _op & comp  #! <--- Caution: do not modify bitwise operator
        return _op

    def visit_xor(self, mapping_object: Any, comparisons: list[Any]):
        return (
            comparisons[0] ^ comparisons[1]
        )  #! <--- Caution: do not modify bitwise operator

    def visit_not(self, mapping_object: Any, comparisons: list[Any]):
        return ~comparisons[0]  #! <--- Caution: do not modify bitwise operator
