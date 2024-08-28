from typing import Any

from python_criteria.filter import Filter

type SQLAlchemyTable = Any

from .attribute import Attribute
from .clauses import BooleanClause, BooleanClauseList
from .filter import ClauseType
from .visitor import BaseVisitor


class MemoryVisitor(BaseVisitor):
    _data: list[dict[Attribute[Any], Any]]
    __current_item: dict[Attribute[Any], Any]

    def __init__(self, data: list[dict[Attribute[Any], Any]]):
        self._data = data

    def _visit_item(self, clause: ClauseType, item: dict[Attribute[Any], Any]) -> Any:
        self.__current_item = item
        name = clause.__class__.__name__.lower()
        method = getattr(self, "visit_" + name)

        if isinstance(clause, BooleanClauseList):
            comparisons = []
            for clause_item in clause.clause_list:
                comparisons.append(self._visit_item(clause_item, item=item))
            return method(comparisons)

        return method(clause)

    def visit(self, _filter: Filter):
        clause = _filter.clause
        if clause is None:
            return self._data

        filtered = []
        for item in self._data:
            if not self._visit_item(clause=clause, item=item):
                continue

            filtered.append(item)

        return filtered

    def _attr(self, field: Attribute[Any]):
        if field not in self.__current_item:
            raise RuntimeError(
                f"Invalid _object_mapping. Missing field '{field.parent_class.__name__}.{field.name}'."
            )

        return self.__current_item[field]

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
        return self._attr(comparison.field) in tuple(comparison.value)

    def visit_like(self, comparison: BooleanClause):
        return comparison.value.lower() in self._attr(comparison.field).lower()

    def visit_notlike(self, comparison: BooleanClause):
        return comparison.value.lower() not in self._attr(comparison.field).lower()

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
        return not comparisons[0]  #! <--- Caution: do not modify bitwise operator
