import abc
from typing import Any

from .clauses import BooleanClause, BooleanClauseList
from .filter import Filter


class BaseVisitor(metaclass=abc.ABCMeta):
    def visit(
        self,
        _filter: Filter,
    ):
        clause = _filter.clause
        if clause is None:
            return None

        name = clause.__class__.__name__.lower()
        method = getattr(self, "visit_" + name)

        if isinstance(clause, BooleanClauseList):
            comparisons = []
            for item in clause.clause_list:
                comparisons.append(self.visit(Filter(item)))

            return method(comparisons)

        return method(clause)

    @abc.abstractmethod
    def visit_eq(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_ne(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_lt(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_le(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_gt(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_ge(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_in(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_like(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_notlike(self, comparison: BooleanClause):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_or(self, comparisons: list[Any]):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_and(self, comparisons: list[Any]):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_xor(self, comparisons: list[Any]):
        raise NotImplementedError

    @abc.abstractmethod
    def visit_not(self, comparisons: list[Any]):
        raise NotImplementedError
