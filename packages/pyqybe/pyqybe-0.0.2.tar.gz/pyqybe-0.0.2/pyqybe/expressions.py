class Eq:
    def __init__(self, column):
        self.column = column

    def equal(self, value):
        return '{} == {}'.format(
            self.column,
            value
        )

    def between(self, arg1, arg2):
        if isinstance(arg1, str):
            arg1 = '\'{}\''.format(arg1)

        if isinstance(arg2, str):
            arg2 = '\'{}\''.format(arg2)

        return '{} BETWEEN {} AND {}'.format(
            self.column,
            arg1,
            arg2
        )