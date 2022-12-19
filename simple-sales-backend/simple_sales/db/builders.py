from typing import Any, LiteralString
from enum import Enum


class SetAssignment:
    def __init__(
        self,
        column_name: LiteralString,
        value: Any,
    ):
        self.column_name = column_name
        self.value = value


class WhereFilter:
    def __init__(
        self,
        column_name: LiteralString,
        operator: LiteralString,
        value: Any,
    ):
        self.column_name = column_name
        self.operator = operator
        self.value = value


class DumbUpdateQueryBuilder:
    def __init__(
        self,
        update_clause: LiteralString,
        returning_clause: LiteralString | None = None,
    ):
        self.update_clause = update_clause
        self.set_assignments: list[SetAssignment] = []
        self.where_filters: list[WhereFilter] = []
        self.returning_clause = returning_clause

    def add_set_assignment(self, column_name: LiteralString, value: Any) -> None:
        self.set_assignments.append(SetAssignment(column_name, value))

    def add_where_filter(
        self, column_name: LiteralString, operator: LiteralString, value: Any
    ) -> None:
        self.where_filters.append(WhereFilter(column_name, operator, value))

    def build(self) -> tuple[str, list[Any]]:
        params: list[Any] = []
        param_number = 0

        def param() -> str:
            nonlocal param_number
            param_number += 1
            return "$" + str(param_number)

        # Build the SET clause

        set_clause_parts = []

        for set_assignment in self.set_assignments:
            set_clause_parts.append(f"{set_assignment.column_name} = {param()}")
            params.append(set_assignment.value)

        set_clause = "SET " + ", ".join(set_clause_parts)

        # Build the WHERE clause

        where_clause_parts = []

        for where_filter in self.where_filters:
            where_clause_parts.append(
                f"{where_filter.column_name} {where_filter.operator} {param()}"
            )
            params.append(where_filter.value)

        where_clause = "WHERE " + " AND ".join(where_clause_parts)

        # Build the query

        query_clauses = [self.update_clause, set_clause, where_clause]

        if self.returning_clause is not None:
            query_clauses.append(self.returning_clause)

        query = "\n".join(query_clauses)

        return query, params
