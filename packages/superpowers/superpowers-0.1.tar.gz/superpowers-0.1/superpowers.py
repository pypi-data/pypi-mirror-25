from forbiddenfruit import curse

def _map(self, fn):
    return list(map(fn, self))

def patch():
    curse(list, 'map', lambda self, fn: list(map(fn, self)))
    curse(tuple, 'map', lambda self, fn: tuple(map(fn, self)))
    curse(list, 'filter', lambda self, fn: list(filter(fn, self)))
    curse(tuple, 'filter', lambda self, fn: tuple(filter(fn, self)))


class Superpower:
    def __init__(self, fn=lambda x: x):
        self.fn = fn

    def __call__(self, val):
        return self.fn(val)

    def __getattr__(self, attr):
        return Superpower(lambda x: getattr(self.fn(x), attr)())

    def __add__(self, other):
        return Superpower(lambda x: self.fn(x) + other)

    def __sub__(self, other):
        return Superpower(lambda x: self.fn(x) - other)

    def __truediv__(self, other):
        return Superpower(lambda x: self.fn(x) / other)

    def __pow__(self, other):
        return Superpower(lambda x: self.fn(x) ** other)

    def __mul__(self, other):
        return Superpower(lambda x: self.fn(x) * other)

    def __eq__(self, other):
        return Superpower(lambda x: self.fn(x) == other)

    def __ne__(self, other):
        return Superpower(lambda x: self.fn(x) != other)

    def __lt__(self, other):
        return Superpower(lambda x: self.fn(x) < other)

    def __le__(self, other):
        return Superpower(lambda x: self.fn(x) <= other)

    def __gt__(self, other):
        return Superpower(lambda x: self.fn(x) > other)

    def __ge__(self, other):
        return Superpower(lambda x: self.fn(x) >= other)

    def __repr__(self):
        return 'Superpower()'

_ = Superpower()
