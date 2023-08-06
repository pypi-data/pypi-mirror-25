class InvalidOperator(BaseException):
    def __init__(self, operator):
        message = 'Invalid operator: %s' % str(operator)
        BaseException.__init__(self, message)
