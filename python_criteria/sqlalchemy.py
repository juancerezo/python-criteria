from typing import Any

type SQLAlchemyTable = Any

from .attribute import Attribute
from .clauses import BooleanClause
from .entity import BaseEntity
from .visitor import BaseVisitor


class SQLAlchemyVisitor(BaseVisitor):
    _entity_table_mapping: dict[type[BaseEntity], Any]

    def __init__(self, entity_table_mapping: dict[type[BaseEntity], type[Any]]):
        self._entity_table_mapping = entity_table_mapping

    def _attr(self, field: Attribute[Any]):
        _table = self._entity_table_mapping.get(field.parent_class)
        if _table is None:
            raise RuntimeError(
                f"Invalid _entity_table_mapping. Missing class '{field.parent_class.__name__}'."
            )

        if not hasattr(_table, field.name):
            raise ValueError(f"'{field.name}' is not a valid attribute of '{field.parent_class.__name__}'")

        return getattr(_table, field.name)

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

    def visit_notlike(self, comparison: BooleanClause):
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
        return comparisons[0] ^ comparisons[1]  #! <--- Caution: do not modify bitwise operator

    def visit_not(self, comparisons: list[Any]):
        return ~comparisons[0]  #! <--- Caution: do not modify bitwise operator
