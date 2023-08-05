import pytest

from kool.db.flatfile import Query


class TestQuery(object):

    def test_no_path(self):
        with pytest.raises(ValueError):
            Query() == 2

    def test_eq(self):
        query = Query().value == 1
        assert query({'value': 1})
        assert not query({'value': 2})
        assert hash(query)

        query = Query().value == [0, 1]
        assert query({'value': [0, 1]})
        assert not query({'value': [0, 1, 2]})
        assert hash(query)

    def test_ne(self):
        query = Query().value != 1
        assert query({'value': 2})
        assert not query({'value': 1})
        assert hash(query)

        query = Query().value != [0, 1]
        assert query({'value': [0, 1, 2]})
        assert not query({'value': [0, 1]})
        assert hash(query)

    def test_lt(self):
        query = Query().value < 1
        assert query({'value': 0})
        assert not query({'value': 1})
        assert hash(query)

    def test_le(self):
        query = Query().value <= 1
        assert query({'value': 0})
        assert query({'value': 1})
        assert not query({'value': 2})
        assert hash(query)

    def test_gt(self):
        query = Query().value > 1
        assert query({'value': 2})
        assert not query({'value': 1})
        assert hash(query)

    def test_ge(self):
        query = Query().value >= 1
        assert query({'value': 2})
        assert query({'value': 1})
        assert not query({'value': 0})
        assert hash(query)

    def test_or(self):
        query = (
            (Query().val1 == 1) |
            (Query().val2 == 2)
        )
        assert query({'val1': 1})
        assert query({'val2': 2})
        assert query({'val1': 1, 'val2': 2})
        assert not query({'val1': '', 'val2': ''})
        assert hash(query)

    def test_and(self):
        query = (
            (Query().val1 == 1) &
            (Query().val2 == 2)
        )
        assert query({'val1': 1, 'val2': 2})
        assert not query({'val1': 1})
        assert not query({'val2': 2})
        assert not query({'val1': '', 'val2': ''})
        assert hash(query)


    def test_not(self):
        query = ~ (Query().val1 == 1)
        assert query({'val1': 5, 'val2': 2})
        assert not query({'val1': 1, 'val2': 2})
        assert hash(query)

        query = (
            (~ (Query().val1 == 1)) &
            (Query().val2 == 2)
        )
        assert query({'val1': '', 'val2': 2})
        assert query({'val2': 2})
        assert not query({'val1': 1, 'val2': 2})
        assert not query({'val1': 1})
        assert not query({'val1': '', 'val2': ''})
        assert hash(query)


    def test_has_key(self):
        query = Query().val3.exists()

        assert query({'val3': 1})
        assert not query({'val1': 1, 'val2': 2})
        assert hash(query)

    def test_custom(self):
        def test(value):
            return value == 42

        query = Query().val.test(test)

        assert query({'val': 42})
        assert not query({'val': 40})
        assert not query({'val': '44'})
        assert not query({'': None})
        assert hash(query)

        def in_list(value, l):
            return value in l

        query = Query().val.test(in_list, tuple([25, 35]))
        assert not query({'val': 20})
        assert query({'val': 25})
        assert not query({'val': 30})
        assert query({'val': 35})
        assert not query({'val': 36})
        assert hash(query)

    def test_custom_with_params(self):
        def test(value, minimum, maximum):
            return minimum <= value <= maximum

        query = Query().val.test(test, 1, 10)

        assert query({'val': 5})
        assert not query({'val': 0})
        assert not query({'val': 11})
        assert not query({'': None})
        assert hash(query)


    def test_any(self):
        query = Query().followers.any(Query().name == 'don')

        assert query({'followers': [{'name': 'don'}, {'name': 'john'}]})
        assert not query({'followers': 1})
        assert not query({})
        assert hash(query)

        query = Query().followers.any(Query().num.matches('\\d+'))
        assert query({'followers': [{'num': '12'}, {'num': 'abc'}]})
        assert not query({'followers': [{'num': 'abc'}]})
        assert hash(query)

        query = Query().followers.any(['don', 'jon'])
        assert query({'followers': ['don', 'greg', 'bill']})
        assert not query({'followers': ['greg', 'bill']})
        assert not query({})
        assert hash(query)

        query = Query().followers.any([{'name': 'don'}, {'name': 'john'}])
        assert query({'followers': [{'name': 'don'}, {'name': 'greg'}]})
        assert not query({'followers': [{'name': 'greg'}]})
        assert hash(query)

    def test_all(self):
        query = Query().followers.all(Query().name == 'don')
        assert query({'followers': [{'name': 'don'}]})
        assert not query({'followers': [{'name': 'don'}, {'name': 'john'}]})
        assert hash(query)

        query = Query().followers.all(Query().num.matches('\\d+'))
        assert query({'followers': [{'num': '123'}, {'num': '456'}]})
        assert not query({'followers': [{'num': '123'}, {'num': 'abc'}]})
        assert hash(query)

        query = Query().followers.all(['don', 'john'])
        assert query({'followers': ['don', 'john', 'greg']})
        assert not query({'followers': ['don', 'greg']})
        assert not query({})
        assert hash(query)

        query = Query().followers.all([{'name': 'john'}, {'age': 17}])
        assert query({'followers': [{'name': 'john'}, {'age': 17}]})
        assert not query({'followers': [{'name': 'john'}, {'age': 18}]})
        assert hash(query)

    def test_hash(self):
        d = {
            Query().key1 == 2: True,
            Query().key1.key2.key3.exists(): True,
            Query().key1.exists() & Query().key2.exists(): True,
            Query().key1.exists() | Query().key2.exists(): True,
        }

        assert (Query().key1 == 2) in d
        assert (Query().key1.key2.key3.exists()) in d
        assert (Query()['key1.key2'].key3.exists()) not in d

        # Commutative property of & and |
        assert (Query().key1.exists() & Query().key2.exists()) in d
        assert (Query().key2.exists() & Query().key1.exists()) in d
        assert (Query().key1.exists() | Query().key2.exists()) in d
        assert (Query().key2.exists() | Query().key1.exists()) in d

    def test_orm_usage(self):
        data = {'name': 'John', 'age': {'year': 2000}}

        User = Query()
        query1 = User.name == 'John'
        query2 = User.age.year == 2000
        assert query1(data)
        assert query2(data)
