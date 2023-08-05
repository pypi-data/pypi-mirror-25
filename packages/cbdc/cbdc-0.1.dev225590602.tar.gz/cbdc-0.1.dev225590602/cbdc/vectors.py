import math
from functools import partial
from operator import mul


__all__ = ['Vector']


class Vector:
    def __init__(self, *values):
        self.values = tuple(values)

    def normalize(self):
        """Return a new vector with the same direction and length normalized
        to 1.

        """
        # multiply with the inverse of its norm
        return (1 / abs(self)) * self

    def __len__(self):
        return len(self.values)

    def __abs__(self):
        return math.sqrt(sum(map(square, self.values)))

    def __add__(self, other):
        return self.__class__(*map(sum, zip(self.values, other.values)))

    # multiply vector with a scalar value
    def __mul__(self, other):
        assert isinstance(other, (int, float))
        return self.__class__(*map(partial(mul, other), self.values))
    __rmul__ = __mul__

    def __repr__(self):
        return '({})'.format(', '.join(map(str, self.values)))


def square(x):
    return x * x


def dotproduct(v1, v2):
    return sum(p*q for p, q in zip(v1.values, v2.values))
