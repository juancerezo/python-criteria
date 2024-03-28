import abc
from typing import Any

from .filter import BooleanClause, BooleanClauseList, FilterableAttribute


class Visitor(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "visit_eq")
            and callable(subclass.visit_eq)
            and hasattr(subclass, "visit_ne")
            and callable(subclass.visit_ne)
            and hasattr(subclass, "visit_lt")
            and callable(subclass.visit_lt)
            and hasattr(subclass, "visit_le")
            and callable(subclass.visit_le)
            and hasattr(subclass, "visit_gt")
            and callable(subclass.visit_gt)
            and hasattr(subclass, "visit_ge")
            and callable(subclass.visit_ge)
            and hasattr(subclass, "visit_in")
            and callable(subclass.visit_in)
            and hasattr(subclass, "visit_like")
            and callable(subclass.visit_like)
            and hasattr(subclass, "visit_not_like")
            and callable(subclass.visit_not_like)
            and hasattr(subclass, "visit_or")
            and callable(subclass.visit_or)
            and hasattr(subclass, "visit_and")
            and callable(subclass.visit_and)
            and hasattr(subclass, "visit_xor")
            and callable(subclass.visit_xor)
            and hasattr(subclass, "visit_not")
            and callable(subclass.visit_not)
            or NotImplemented
        )

    def visit(
        self,
        filter_or_comparison: FilterableAttribute | BooleanClause | BooleanClauseList,
    ):
        name = filter_or_comparison.__class__.__name__.lower()
        method = getattr(self, "visit_" + name)

        if isinstance(filter_or_comparison, BooleanClauseList):
            comparisons = []
            for _filter in filter_or_comparison.clause_list:
                comparisons.append(self.visit(_filter))

            return method(comparisons)

        return method(filter_or_comparison)

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
    def visit_not_like(self, comparison: BooleanClause):
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
