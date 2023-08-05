import os
import pytest

from kool.db.flatfile import FlatFileDB, Table, where

TESTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestFlatFile(object):

    @classmethod
    def setup_class(cls):
        testdb = os.path.join(TESTS_DIR, 'fixtures')
        cls.db = FlatFileDB(path=testdb)
        cls.db.purge_table('.meta')

    def test_one_table(self):
        table1 = self.db.create_table('table1')

        table1.insert_multiple({'int': 1, 'char': c} for c in 'abc')

        assert table1.get(where('int') == '1')['char'] == 'a'
        assert table1.get(where('char') == 'b')['char'] == 'b'

        table1.purge()
        assert len(table1) == 0

    def test_multiple_tables(self):
        table1 = self.db.create_table('table1')
        table2 = self.db.create_table('table2')
        table3 = self.db.create_table('table3')

        table1.insert({'int': 1, 'char': 'a'})
        table2.insert({'int': 1, 'char': 'b'})
        table3.insert({'int': 1, 'char': 'c'})

        assert table1.count(where('char') == 'a') == 1
        assert table2.count(where('char') == 'b') == 1
        assert table3.count(where('char') == 'c') == 1

        self.db.purge_table('table1')
        self.db.purge_table('table2')
        self.db.purge_table('table3')

        assert len(table1) == 0
        assert len(table2) == 0
        assert len(table3) == 0

    def test_table(self):
        table = self.db.table('table1')
        assert isinstance(table, Table)

    def test_tables(self):
        assert len(self.db.tables()) == 3
        assert isinstance(self.db.tables()[0], Table)

    def test_table_is_iterable(self):
        table = self.db.table('table1')
        table.insert_multiple({'int': i} for i in range(3))
        assert [r for r in table] == table.all()
        table.purge()
        assert len(table) == 0

    def test_table_get(self):
        table = self.db.table('table1')
        table.insert({'int': 1, 'char': 'a'})
        table.insert({'int': 2, 'char': 'b'})
        table.insert({'int': 3, 'char': 'c'})
        assert table.get(rid=2)['char'] == 'b'
        assert table.get(cond=(where('char') == 'a'))['int'] == '1'
        table.purge()
        assert len(table) == 0        
