from pyqybe.operators import Operator, OperatorParser


class Expression(list):
    def __init__(self, *expressions, order=None, join_str):
        super().__init__()
        self._expressions = []
        self.join_str = join_str
        self.parse_expressions(*expressions, order=order)

    def parse_expressions(self, *expressions, order):
        equations = []
        for expression in expressions:
            if isinstance(expression, list):
                equations.extend(expression)
            else:
                equations.extend(self._parse_expression(expression, order))

        self.extend(equations)

    def add(self, *expressions):
        self.extend(*expressions)
        return self

    @staticmethod
    def _parse_expression(expression, order=None):
        equations = []
        if not order:
            order = expression.keys()

        for column in order:
            operator, value = Operator.sniff(expression[column])
            equations.append(OperatorParser(operator).parse(column, value))

        return equations

    def extend(self, equations):
        self_contain = True if len(equations) > 1 else False

        formatted_equation = ' {} '.format(self.join_str).join(equations)
        if self_contain:
            formatted_equation = '({})'.format(formatted_equation)

        super().append(formatted_equation)


class Ex(Expression):
    JOIN_STR = 'AND'

    def __init__(self, *expressions, order=None):
        super().__init__(*expressions, order=order, join_str=self.JOIN_STR)


class ExOr(Expression):
    JOIN_STR = 'OR'

    def __init__(self, *expressions, order=None):
        super().__init__(*expressions, order=order, join_str=self.JOIN_STR)
