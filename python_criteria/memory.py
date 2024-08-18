from typing import Any

type SQLAlchemyTable = Any

from .clauses import BooleanClause
from .entity import BaseEntity
from .filter import Attribute
from .visitor import BaseVisitor


class MemoryVisitor(BaseVisitor):
    _attribute_table_column_mapping: dict[type[BaseEntity], Any]

    def __init__(self, _attribute_table_column_mapping: dict[type[BaseEntity], Any]):
        self._attribute_table_column_mapping = _attribute_table_column_mapping

    def _attr(self, field: Attribute[Any]):
        _object = self._attribute_table_column_mapping.get(field.parent_class)
        if _object is None:
            raise RuntimeError(
                f"Invalid _object_mapping. Missing class '{field.parent_class.__name__}'."
            )

        if not hasattr(_object, field.name):
            raise ValueError(
                f"'{field.name}' is not a valid attribute of '{field.parent_class.__name__}'"
            )

        return getattr(_object, field.name)

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
