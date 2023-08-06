from .expressions import (
    Ex,
    ExOr
)
from .operators import Operator
from .oracle_query_builder import OracleQueryBuilder
from .statements import (
    Select,
    Where,
    OrderBy,
    From,
    GroupBy,
    Having,
    Statement
)

ex = ex_and = Ex
ex_or = ExOr
op = Operator
query = OracleQueryBuilder

__author__ = 'Eryk Humberto Oliveira Alves'
__email__ = 'erykwho@gmail.com'
__version__ = '0.0.3'
