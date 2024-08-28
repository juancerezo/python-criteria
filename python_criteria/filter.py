# pyright: reportAttributeAccessIssue=false, reportIncompatibleMethodOverride=false
from typing import Any, TypeVar

from .clauses import BooleanClause, BooleanClauseList

type ClauseType = BooleanClause | BooleanClauseList
_T_co = TypeVar("_T_co", bound=Any, covariant=True)


class Filter:
    __clauses: ClauseType | None

    def __init__(self, clause: ClauseType | None = None) -> None:
        self.__clauses = clause

    def __and__(self, clause: ClauseType):
        if self.__clauses is None:
            self.__clauses = clause

        self.__clauses = self.__clauses & clause

        return self

    def __or__(self, clause: ClauseType):
        if self.__clauses is None:
            self.__clauses = clause

        self.__clauses = self.__clauses | clause

        return self

    @property
    def clause(self):
        return self.__clauses
