class Typed(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __eq__(self, other):
        return (
            isinstance(other, Typed) and
            other.name == self.name and
            other.value == self.value
        )
