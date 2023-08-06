import collections

from .components import (
    Select,
    Where,
    GroupBy,
    Having,
    OrderBy,
)
from .utils import clean_query


class OracleQueryBuilder:
    COMPONENT_ORDER = {
        1: Select,
        2: Where,
        3: GroupBy,
        4: Having,
        5: OrderBy
    }

    def __init__(self):
        self.components = {
            Select: [],
        }

    def __str__(self):
        return self.build_query()

    @property
    def query(self):
        return self.build_query()

    @property
    def plain_query(self):
        return clean_query(self.build_query())

    def select(self, *args, **kwargs):
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

        :param kwargs: Columns to select if you wish to attribute an alias to the columns
            example:
                with the following key arguments
                    kwargs = {FIXED_COLUMN='1', REFERENCE_DAY=REFERENCE_DAY}
                the parsed query will be
                    SELECT
                        1               AS FIXED_COLUMN,
                        REFERENCE_DAY   AS REFERENCE_DAY
        :return: An OracleQueryBuilder object with the component SELECT
        """
        self.components[Select].append(
            *args,
            *['{} AS {}'.format(value, column) for column, value in kwargs.items()]
        )

        return self

    def from_table(self, *args):
        pass

    def build_query(self):
        query = ''
        ordered_components = collections.OrderedDict(sorted(self.COMPONENT_ORDER.items()))
        for _, component in ordered_components.items():
            query += component().parse(self.components.get(component))

        return query
