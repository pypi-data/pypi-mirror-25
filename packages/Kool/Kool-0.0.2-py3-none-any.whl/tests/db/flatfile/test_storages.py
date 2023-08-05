import os
import pytest

from kool.db.flatfile import CSVStorage

element = {
            1: {'fruit': 'apple', 'cost': 100},
            2: {'fruit': 'banana', 'cost': 200},
          }

expected = {
            '1': {'_id': '1', 'cost': '100', 'fruit': 'apple'},
            '2': {'_id': '2', 'cost': '200', 'fruit': 'banana'}
           }
        

TESTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCSVStorage(object):

    @classmethod
    def setup_class(cls):
        cls.db_path = os.path.join(TESTS_DIR, 'fixtures')
        cls.file_path = os.path.join(cls.db_path, 'file1')
        
    def test_create_db(self):
        storage = CSVStorage(path=self.file_path, init_db=True)
        assert storage.path == self.db_path
        new_file = str(self.file_path) + '.csv'
        assert os.path.isfile(new_file)

    def test_read_write(self):
        storage = CSVStorage(path=self.file_path, init_db=True)
        # Write data
        storage.write(element)

        # Verify data
        assert expected == storage.read()
        storage.close()
