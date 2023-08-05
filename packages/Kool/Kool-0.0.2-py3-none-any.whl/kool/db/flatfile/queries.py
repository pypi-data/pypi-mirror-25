"""
Contains the querying interface.

FlatFileDB query implementation is a variant of TinyDB query.
TinyDB is a lightweight document oriented database written in pure 
python with no external depedencies.

Repo: https://github.com/msiemens/tinydb
"""

import re
import sys

from .utils import catch_warning, freeze

__all__ = ('Query', 'where')


def is_sequence(obj):
    """Check if object has an iterator

    :param obj: 
    """
    return hasattr(obj, '__iter__')


class QueryImpl(object):
    """A query implementation.
    
    This query implementation wraps a test function which is run when the
    query is evaluated by calling the object.
    
    Queries can be combined with logical and/or and modified with logical not.
    """
    def __init__(self, test, hashval):
        self.test = test
        self.hashval = hashval

    def __call__(self, value):
        return self.test(value)

    def __hash__(self):
        return hash(self.hashval)

    def __repr__(self):
        return 'QueryImpl{0}'.format(self.hashval)

    def __eq__(self, other):
        return self.hashval == other.hashval

    def __and__(self, other):
        # We use a frozenset for the hash as the AND operation is commutative
        # (a | b == b | a)
        return QueryImpl(lambda value: self(value) and other(value),
                         ('and', frozenset([self.hashval, other.hashval])))

    def __or__(self, other):
        # We use a frozenset for the hash as the OR operation is commutative
        # (a & b == b & a)
        return QueryImpl(lambda value: self(value) or other(value),
                         ('or', frozenset([self.hashval, other.hashval])))

    def __invert__(self):
        return QueryImpl(lambda value: not self(value),
                         ('not', self.hashval))


class Query(object):
    """FlatFileDB Queries.
    
    Provides a way of writing queries for FlatFileDB.
    """

    def __init__(self):
        self._path = []

    def __getattr__(self, item):
        query = Query()
        query._path = self._path + [item]

        return query

    __getitem__ = __getattr__

    def _generate_test(self, test, hashval):
        """Generate a query based on a test function.

        :param test: type
        :param hashval: type
        :returns: obj: QueryImpl -- A QueryImpl obj
        :raises ValueError: Query has no path
        
        """
        if not self._path:
            raise ValueError('Query has no path')

        def impl(value):
            """

            :param value: 

            """
            try:
                # Resolve the path
                for part in self._path:
                    value = value[part]
            except (KeyError, TypeError):
                return False
            else:
                return test(value)

        return QueryImpl(impl, hashval)

    def __eq__(self, rhs):
        """
        Test a dict value for equality.

        >>> Query().f1 == 42

        :param rhs: The value to compare against
        
        [description]
        
        Arguments:
            rhs {[type]} -- [description]
        
        Returns:
            [type] -- [description]
        """
        if sys.version_info <= (3, 0):  # pragma: no cover
            # Special UTF-8 handling on Python 2
            def test(value):
                """

                :param value: 

                """
                with catch_warning(UnicodeWarning):
                    try:
                        return value == rhs
                    except UnicodeWarning:
                        # Dealing with a case, where 'value' or 'rhs'
                        # is unicode and the other is a byte string.
                        if isinstance(value, str):
                            return value.decode('utf-8') == rhs
                        elif isinstance(rhs, str):
                            return value == rhs.decode('utf-8')

        else:  # pragma: no cover
            def test(value):
                """

                :param value: 

                """
                return value == rhs

        return self._generate_test(lambda value: test(value),
                                   ('==', tuple(self._path), freeze(rhs)))

    def __ne__(self, rhs):
        """
        Test a dict value for inequality.

        >>> Query().f1 != 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value != rhs,
                                   ('!=', tuple(self._path), freeze(rhs)))

    def __lt__(self, rhs):
        """
        Test a dict value for being lower than another value.

        >>> Query().f1 < 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value < rhs,
                                   ('<', tuple(self._path), rhs))

    def __le__(self, rhs):
        """
        Test a dict value for being lower than or equal to another value.

        >>> where('f1') <= 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value <= rhs,
                                   ('<=', tuple(self._path), rhs))

    def __gt__(self, rhs):
        """
        Test a dict value for being greater than another value.

        >>> Query().f1 > 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value > rhs,
                                   ('>', tuple(self._path), rhs))

    def __ge__(self, rhs):
        """
        Test a dict value for being greater than or equal to another value.

        >>> Query().f1 >= 42

        :param rhs: The value to compare against
        """
        return self._generate_test(lambda value: value >= rhs,
                                   ('>=', tuple(self._path), rhs))

    def exists(self):
        """Test for a dict where a provided key exists.

        :param rhs: The value to compare against

        >>> Query().f1.exists() >= 42
        """
        return self._generate_test(lambda _: True,
                                   ('exists', tuple(self._path)))

    def matches(self, regex):
        """Run a regex test against a dict value (whole string has to match).

        :param regex: The regular expression to use for matching

        >>> Query().f1.matches(r'^\w+$')
        """
        return self._generate_test(lambda value: re.match(regex, value),
                                   ('matches', tuple(self._path), regex))

    def filter(self, regex):
        """Run a regex test against a dict value (only substring string has to
        match).

        :param regex: The regular expression to use for matching

        >>> Query().f1.filter(r'^\w+$')
        """
        return self._generate_test(lambda value: re.filter(regex, value),
                                   ('filter', tuple(self._path), regex))

    def test(self, func, *args):
        """Run a user-defined test function against a dict value.

        :param func: The function to call, passing the dict as the first
                     argument
        :param args: Additional arguments to pass to the test function
        :param *args: 

        >>> def test_func(val):
        ...     return val == 42
        ...
        >>> Query().f1.test(test_func)
        """
        return self._generate_test(lambda value: func(value, *args),
                                   ('test', tuple(self._path), func, args))

    def any(self, cond):
        """Checks if a condition is met by any record in a list,
        where a condition can also be a sequence (e.g. list).
        
        
        Matches::
        
            {'f1': [{'f2': 1}, {'f2': 0}]}
        
        
        Matches::
        
            {'f1': [1, 2]}
            {'f1': [3, 4, 5]}

        :param cond: Either a query that at least one record has to match or
                     a list of which at least one record has to be contained
                     in the tested record.

        >>> Query().f1.any(Query().f2 == 1)
        
        >>> Query().f1.any([1, 2, 3])
        # Match f1 that contains any record from [1, 2, 3]
        """
        if callable(cond):
            def _cmp(value):
                """

                :param value: 

                """
                return is_sequence(value) and any(cond(e) for e in value)

        else:
            def _cmp(value):
                """

                :param value: 

                """
                return is_sequence(value) and any(e in cond for e in value)

        return self._generate_test(lambda value: _cmp(value),
                                   ('any', tuple(self._path), freeze(cond)))

    def all(self, cond):
        """Checks if a condition is met by any record in a list,
        where a condition can also be a sequence (e.g. list).
        
        
        Matches::
        
            {'f1': [{'f2': 1}, {'f2': 1}]}
        
        
        Matches::
        
            {'f1': [1, 2, 3, 4, 5]}

        :param cond: Either a query that all records have to match or a list
                     which has to be contained in the tested record.

        >>> Query().f1.all(Query().f2 == 1)
        
        >>> Query().f1.all([1, 2, 3])
        # Match f1 that contains any record from [1, 2, 3]
        """
        if callable(cond):
            def _cmp(value):
                """

                :param value: 

                """
                return is_sequence(value) and all(cond(e) for e in value)

        else:
            def _cmp(value):
                """

                :param value: 

                """
                return is_sequence(value) and all(e in value for e in cond)

        return self._generate_test(lambda value: _cmp(value),
                                   ('all', tuple(self._path), freeze(cond)))


def where(key):
    """

    :param key: 

    """
    return Query()[key]
