try:
    from collections import UserDict
except ImportError:
    # python2
    class UserDict(object):  # pragma: no_cover
        def __init__(self):  # pragma: no cover
            self.data = {}  # pragma: no cover

from .errors import ParameterNotSetError


class ParameterMap(UserDict):
    """A subclass of ``UserDict`` to hold key/value pairs for params
    in Cypher Queries."""
    def __init__(self, keys=None):
        """Initialize from a ParameterSet to create an empty mapping of
        parameters.

        :param keys: iterable of parameter names
        """
        UserDict.__init__(self)
        self._keys = keys if keys is not None else ParameterSet()

    def keys(self):
        return self._keys

    def items(self):
        return [(k, self[k]) for k in self.keys()]

    def iteritems(self):
        return self.items()

    def __repr__(self):
        return 'ParameterMap({0})'.format(repr({
            k:self[k]
            for k in self.keys()
        }))

    def __str__(self):
        return repr(self)

    def __setitem__(self, k, v):
        if k not in self.keys():
            raise ParameterNotSetError((
                'Parameters can only be set if they are already specified '
                'in the cypher query.'
            ))
        self.data[k] = v

    def __getitem__(self, k):
        try:
            return self.data[k]
        except KeyError:
            if k in self.keys():
                return None

        raise ParameterNotSetError((
            'The parameter you specified was not found in your query.'
        ))

    def __iter__(self):
        return iter(self.keys())

    def __len__(self):
        return len(self.keys())

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        for k, v in self.items():
            if other[k] != v:
                return False

        return True

    def __ne__(self, other):
        return not(self.__eq__(other))

    def __bool__(self):
        return len(self) > 0

    def __contains__(self, item):
        return item in self.keys()


class ParameterSet(set):
    """A subclass of ``set`` to hold parameter keys"""
    pass
