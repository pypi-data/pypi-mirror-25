class Statement:
    def __init__(self, statement_str='', *elements, sep=', '):
        self.sep = sep
        self.statement_str = statement_str
        self._elements = list(elements)

    def add(self, *elements):
        self._elements.extend(elements)
        return self

    def parse(self):
        if not self._elements:
            return ''

        return '{statement} {elements} '.format(
            statement=self.statement_str,
            elements='{sep} '.format(sep=self.sep).join(
                '{}'.format(value) for value in self._elements)
        )


class Select(Statement):
    STATEMENT_STR = 'SELECT'

    def __init__(self, *elements):
        super().__init__(self.STATEMENT_STR, *elements)


class Where(Statement):
    STATEMENT_STR = 'WHERE'
    SEP = ' AND '

    def __init__(self, *elements):
        super().__init__(self.STATEMENT_STR, *elements, sep=self.SEP)


class From(Statement):
    STATEMENT_STR = 'FROM'

    def __init__(self, *elements):
        super().__init__(self.STATEMENT_STR, *elements)


class GroupBy(Statement):
    pass


class Having(Statement):
    pass


class OrderBy(Statement):
    pass
