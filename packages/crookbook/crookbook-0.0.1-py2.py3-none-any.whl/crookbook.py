import six


def essence(attrs, mutable=True):

    def essence_maker(cls):

        def __essence__(self):
            return tuple(getattr(self, attr) for attr in attrs)

        setattr(cls, '__essence__', __essence__)

        def eq(self, other):
            if isinstance(other, cls):
                return self.__essence__() == cls.__essence__(other)
            return NotImplemented

        setattr(cls, '__eq__', eq)

        if six.PY2:

            # Taken from:
            #   https://stackoverflow.com/a/35781654
            def ne(self, other):
                equal = self.__eq__(other)
                return equal if equal is NotImplemented else not equal

            setattr(cls, '__ne__', ne)

        def hash_(self):
            return hash(self.__essence__())

        setattr(cls, '__hash__', None if mutable else hash_)

        # Would use total_ordering, but the recursive comparison issue is still present in
        # Python 2.7, so have to work this way instead.
        def lt(self, other):
            if isinstance(other, cls):
                return self.__essence__() < cls.__essence__(other)
            return NotImplemented

        def le(self, other):
            if isinstance(other, cls):
                return self.__essence__() <= cls.__essence__(other)
            return NotImplemented

        def gt(self, other):
            if isinstance(other, cls):
                return self.__essence__() > cls.__essence__(other)
            return NotImplemented

        def ge(self, other):
            if isinstance(other, cls):
                return self.__essence__() >= cls.__essence__(other)
            return NotImplemented

        setattr(cls, '__lt__', lt)
        setattr(cls, '__le__', le)
        setattr(cls, '__gt__', gt)
        setattr(cls, '__ge__', ge)
        return cls

    return essence_maker


def described(inner):

    def described_maker(cls):

        def repr_(self):
            return ('<{0.__class__.__name__} ' + inner + '>').format(self)

        setattr(cls, '__repr__', repr_)

        if '__str__' not in cls.__dict__:
            def str_(self):
                return repr(self)
            setattr(cls, '__str__', str_)

        return six.python_2_unicode_compatible(cls)

    return described_maker
