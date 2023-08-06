class ComponentParser:
    def parse(self, values):
        if not values:
            return ''


class Select(ComponentParser):
    COMPONENT_STR = 'SELECT'

    def parse(self, values=None):
        if not values:
            return ''

        return '{component}\n{values}\n'.format(
            component=self.COMPONENT_STR,
            values='\n'.join('\t{}'.format(value) for value in values)
        )


class Where(ComponentParser):
    pass


class From(ComponentParser):
    pass


class GroupBy(ComponentParser):
    pass


class Having(ComponentParser):
    pass


class OrderBy(ComponentParser):
    pass
