"""
FlatFileDB

A simple csv storage flatfile database.

A variant of TinyDB by @msiemens
Repo: https://github.com/msiemens/tinydb
"""
from .queries import Query, where
from .storages import Storage, CSVStorage
from .database import FlatFileDB, Table

__all__ = ('FlatFileDB', 'Table', 'Storage', 'CSVStorage', 'Query', 'where')