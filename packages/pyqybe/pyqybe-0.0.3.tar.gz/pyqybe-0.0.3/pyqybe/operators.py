from pyqybe.exceptions import InvalidOperator

EQUAL_OPERATOR_STR = 'equal'
BIGGER_OPERATOR_STR = 'bigger'
BIGGER_OR_EQUAL_OPERATOR_STR = 'bigger or equal'
SMALLER_OPERATOR_STR = 'smaller'
SMALLER_OR_EQUAL_OPERATOR_STR = 'smaller or equal'
DIFFERENT_OPERATOR_STR = 'different'
IN_OPERATOR_STR = 'in'
LIKE_OPERATOR_STR = 'like'
BETWEEN_OPERATOR_STR = 'between'
ALL_OPERATORS_STR = [EQUAL_OPERATOR_STR, BIGGER_OPERATOR_STR, BIGGER_OR_EQUAL_OPERATOR_STR, SMALLER_OPERATOR_STR,
                 SMALLER_OR_EQUAL_OPERATOR_STR, DIFFERENT_OPERATOR_STR, IN_OPERATOR_STR, LIKE_OPERATOR_STR,
                 BETWEEN_OPERATOR_STR,
                 ]


class Operator:
    @staticmethod
    def like(value):
        """
            LIKE operator
                NAME LIKE '%WORKER%'
        :param value: the 2nd term of the expression
            For the example above, it would be '%WORKER%'
        :return: tuple containing the operator string and the 2nd term of the expression
        """
        return LIKE_OPERATOR_STR, value

    @staticmethod
    def equal(value):
        """
            Equality operator
                CITY == 'Uberaba'
        :param value: the 2nd term of the expression
            For the example above, it would be 'Uberaba'
        :return: tuple containing the operator string and the 2nd term of the expression
        """
        return EQUAL_OPERATOR_STR, value

    @staticmethod
    def bigger(value):
        return BIGGER_OPERATOR_STR, value

    @staticmethod
    def bigger_or_equal(value):
        return BIGGER_OR_EQUAL_OPERATOR_STR, value

    @staticmethod
    def smaller(value):
        return SMALLER_OPERATOR_STR, value

    @staticmethod
    def smaller_or_equal(value):
        return SMALLER_OR_EQUAL_OPERATOR_STR, value

    @staticmethod
    def different(value):
        return DIFFERENT_OPERATOR_STR, value

    @staticmethod
    def between(first, second):
        """
            BETWEEN operator
                REFERENCE_DATE BETWEEN '20170701' AND '20170731'
        :param first: the 1st value of the 2nd term of the expression
            For the example above, it would be '20170701'
        :param second: the 1st value of the 2nd term of the expression
            For the example above, it would be '20170731'
        :return: tuple containing the operator string and the 2nd term of the expression
        """
        return BETWEEN_OPERATOR_STR, (first, second)

    @staticmethod
    def in_operator(*values):
        """
            IN operator
                COUNTRY IN ('BRAZIL', 'NETHERLANDS', 'FINLAND')
        :param values: the 2nd term of the expression
            Lists and tuples are accepted
            For the example above, it would be either:
                ['BRAZIL', 'NETHERLANDS', 'FINLAND']
                or 'BRAZIL', 'NETHERLANDS', 'FINLAND'
        :return: tuple containing the operator string and the 2nd term of the expression
        """
        operator_values = []
        for value in values:
            if isinstance(value, list):
                operator_values.extend(value)
            else:
                operator_values.append(value)

        return IN_OPERATOR_STR, operator_values

    @staticmethod
    def sniff(*expression):
        """
            sniff will the operator for the expression
        :param expression: The expression to be looked up
            Examples:
                i) 1,
                ii) 1, 2, 3
                iii) [1, 2, 3]
                iv) equal(5)
        :return: tuple containing the operator string and the expression
        """

        if len(expression) == 1:
            expression = expression[0]

            if isinstance(expression, tuple):
                if expression[0] in ALL_OPERATORS_STR:
                    return expression[0], expression[1]
                else:
                    raise InvalidOperator(expression)

            if isinstance(expression, list):
                return IN_OPERATOR_STR, expression

            return EQUAL_OPERATOR_STR, expression

        else:
            if isinstance(expression, tuple):
                return IN_OPERATOR_STR, [el for el in expression]


class OperatorParser:
    # Templates
    EQUAL_TEMPLATE = '{} == {}'
    BIGGER_TEMPLATE = '{} > {}'
    BIGGER_OR_EQUAL_TEMPLATE = '{} >= {}'
    SMALLER_TEMPLATE = '{} < {}'
    SMALLER_OR_EQUAL_TEMPLATE = '{} <= {}'
    DIFFERENT_TEMPLATE = '{} <> {}'
    IN_TEMPLATE = '{} IN ({})'
    LIKE_TEMPLATE = '{} LIKE {}'
    BETWEEN_TEMPLATE = '{} BETWEEN {} AND {}'

    def __init__(self, operator=None):
        self.operator = operator

        self.parsers = {
            EQUAL_OPERATOR_STR: self.equal,
            BIGGER_OPERATOR_STR: self.bigger,
            BIGGER_OR_EQUAL_OPERATOR_STR: self.bigger_or_equal,
            SMALLER_OPERATOR_STR: self.smaller,
            SMALLER_OR_EQUAL_OPERATOR_STR: self.smaller_or_equal,
            DIFFERENT_OPERATOR_STR: self.different,
            IN_OPERATOR_STR: self.in_operator,
            LIKE_OPERATOR_STR: self.like,
            BETWEEN_OPERATOR_STR: self.between
        }

    def parse(self, column, *args):
        return self.parsers[self.operator](column, *args)

    def equal(self, column, value):
        return self.EQUAL_TEMPLATE.format(
            column,
            self.parse_type(value)
        )

    def bigger(self, column, value):
        return self.BIGGER_TEMPLATE.format(
            column,
            self.parse_type(value)
        )

    def bigger_or_equal(self, column, value):
        return self.BIGGER_OR_EQUAL_TEMPLATE.format(
            column,
            self.parse_type(value)
        )

    def smaller(self, column, value):
        return self.SMALLER_TEMPLATE.format(
            column,
            self.parse_type(value)
        )

    def smaller_or_equal(self, column, value):
        return self.SMALLER_OR_EQUAL_TEMPLATE.format(
            column,
            self.parse_type(value)
        )

    def different(self, column, value):
        return self.DIFFERENT_TEMPLATE.format(
            column,
            self.parse_type(value)
        )

    def in_operator(self, column, values):
        return self.IN_TEMPLATE.format(
            column,
            ', '.join(self.parse_type(value) for value in values),
        )

    def like(self, column, value):
        return self.LIKE_TEMPLATE.format(
            column,
            self.parse_type(value)
        )

    def between(self, column, *values):
        # TODO: Find a better way for this approach: values = values[0]
        values = values[0]
        return self.BETWEEN_TEMPLATE.format(
            column,
            self.parse_type(values[0]),
            self.parse_type(values[1])
        )

    @staticmethod
    def parse_type(value):
        if isinstance(value, str):
            return '\'{}\''.format(value)

        return str(value)
