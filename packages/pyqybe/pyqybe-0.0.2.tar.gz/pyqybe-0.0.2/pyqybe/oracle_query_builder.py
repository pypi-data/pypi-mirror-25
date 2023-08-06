import collections

from .statements import (
    Select,
    From,
    Where,
    GroupBy,
    Having,
    OrderBy,
)
from .utils import clean_query


class OracleQueryBuilder:
    COMPONENT_ORDER = {
        1: Select,
        2: From,
        3: Where,
        4: GroupBy,
        5: Having,
        6: OrderBy
    }

    def __init__(self):
        self.statements = {}

    def __str__(self):
        return self.build_query()

    @property
    def query(self):
        return self.build_query()

    @property
    def plain_query(self):
        return clean_query(self.build_query())

    def select(self, *args):
        """
        This method will receive arguments and key arguments
        for columns and aliased for columns for the
        OracleQueryBuilder object
        :param args: Columns to select
            example:
                with the following arguments
                    args = FOO, BAR
                the parsed query will be
                    SELECT
                        FOO,
                        BAR

        :return: An OracleQueryBuilder object with the component SELECT
        """
        if not self.statements.get(Select):
            self.statements[Select] = Select()

        self.statements[Select].add(*args)

        return self

    def from_table(self, *args):
        if not self.statements.get(From):
            self.statements[From] = From()

        self.statements[From].add(*args)

        return self

    def build_query(self):
        query = ''
        ordered_statements = collections.OrderedDict(sorted(self.COMPONENT_ORDER.items()))
        for _, statement in ordered_statements.items():
            statement_instance = self.statements.get(statement)
            if statement_instance:
                query += statement_instance.parse()

        return query
