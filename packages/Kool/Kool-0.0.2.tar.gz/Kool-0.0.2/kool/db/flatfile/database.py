"""
FlatFileDB

This is a simple flat file database implementation. 

FlatFileDB is a variant of TinyDB that focuses on csv storage.
TinyDB is a lightweight document oriented database written in pure 
python with no external depedencies.

Repo: https://github.com/msiemens/tinydb
"""
import os
from . import CSVStorage
from .utils import LRUCache, iteritems, itervalues

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Record(dict):
    """Represents a record stored in a table.
    
    Records are composed of fields.
    Each record provides a unique way of accessing it
    by use of ``rid`` field which is a proxy to the ``_id``
    column in the table.


    """
    def __init__(self, value=None, rid=None, **kwargs):
        super(Record, self).__init__(**kwargs)

        if value is not None:
            self.update(value)
            self.rid = rid


class StorageProxy(object):
    """Storage proxy handles data conversion"""
    
    def __init__(self, flatfiledb, table_name):
        self._database = flatfiledb._database
        self._storage = flatfiledb._storage
        self._table_name = table_name
        
        # Prepare the storage 
        self._opened = True

        # Initialize a table
        table_path = os.path.join(self._database.path, self._table_name)
        self._table = self._storage(table_path,  create_dirs=True)

    def read(self):
        """Reads from the storage and converts data to a
        dictionary of Records


        """
        try:
            raw_data = self._table.read() or {}
        except KeyError:
            return {}

        data = {}
        for key, val in iteritems(raw_data):
            rid = int(key)
            data[rid] = Record(val, rid)

        return data

    def write(self, values):
        """Writes received values to storage.

        :param values: 

        """
        data = self._table.read() or {}
        self._table.write(values)

    def purge(self):
        """Truncates the entire table"""
        self._table.purge()

    def close(self):
        """Closes table file connection"""
        self._opened = False
        self._table.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._opened is True:
            self.close()


class FlatFileDB(object):
    """FlatFileDB database main class.
    
    Provides access to methods of operating the database.


    """
    DEFAULT_DB = '.ffdb'
    DEFAULT_TABLE = '_default_table'
    DEFAULT_STORAGE = CSVStorage
    _storage = None
    _database = None

    def __init__(self, name=DEFAULT_DB, *args, **kwargs):
        """Create a new database.
        
        All arguments and keyword arguments will be passed to the underlying
        storage class
        """
        
        # supports first argument as database name
        self.name = name or (args[0] if args else None)

        storage = kwargs.pop('storage', FlatFileDB.DEFAULT_STORAGE)
        table = kwargs.pop('default_table', FlatFileDB.DEFAULT_TABLE)
        default_path = os.path.join(PROJECT_ROOT, self.name)
        path = kwargs.pop('path', default_path)

        # Prepare the storage 
        self._opened = True
        
        # Define storage
        FlatFileDB._storage = storage

        # Create database
        FlatFileDB._database = storage(os.path.join(path, '.meta'), 
            init_db=True, create_dirs=True, **kwargs)
        
        self._table_cache = {}
        
        # Define tables
        self._tables = {}
        self._table = None

        data = FlatFileDB._database.read() or {}
        if data:
            self._last_id = max(i for i in data)
        else:
            self._last_id = 0

    def create_table(self, name=DEFAULT_TABLE, *args, **kwargs):
        """Creates a new table, if it doesn't exist, otherwise
        it returns the cached table.

        :param args: param kwargs:
        :param Keyword: Arguments
        :param name: str (Default value = DEFAULT_TABLE)
        :param *args: 
        :param **kwargs: 

        """

        # supports first argument as table name
        name = name or (args[0] if args else None)

        if name in self._table_cache:
            return self._table_cache[name]

        self._table = self.table_class(StorageProxy(FlatFileDB, name), **kwargs)

        self._table_cache[name] = self._table

        self._tables = FlatFileDB._database.read() or {}

        self._tables[self._get_next_id()] = {'table': name}
        
        FlatFileDB._database.write(self._tables)
        
        return self._table

    def table(self, name=DEFAULT_TABLE, *args, **kwargs):
        """Get access to a specific table.

        :param args: param kwargs: extra options
        :param Keyword: Arguments
        :param name: str (Default value = DEFAULT_TABLE)
        :param *args: 
        :param **kwargs: 
        :returns: Table] -- a table object

        """

        # supports first argument as table name
        name = name or (args[0] if args else None)

        if name in self._table_cache:
            return self._table_cache[name]

        self._table = self.table_class(StorageProxy(FlatFileDB, name), **kwargs)

        return self._table

    def tables(self):
        """Get a dict of table objects.


        :returns: list[Table]] -- a list of table objects

        """
        tbls = []
        meta_data = FlatFileDB._database.read() or {}

        for k, v in meta_data.items():
            tbls.append(self.table_class(StorageProxy(FlatFileDB, v['table'])))

        return tbls

    def purge_table(self, name):
        """Purge a specific table from the database. **CANNOT BE REVERSED!**

        :param name: str

        """
        if name in self._table_cache:
            del self._table_cache[name]

        proxy = StorageProxy(FlatFileDB, name)
        proxy.purge()

    def close(self):
        """ """
        self._opened = False
        self._table.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if self._opened is True:
            self.close()

    def _get_next_id(self):
        """Increment the ID used the last time and return it."""
        current_id = int(self._last_id) + 1
        self._last_id = current_id

        return current_id

    def __len__(self):
        """Get the total number of records in the database."""
        return len(self._tables)
    
    
class Table(object):
    """Represents a single FlatFileDB table"""

    def __init__(self, storage, cache_size=10):
        """Initialize a table
        
        :param storage: StorageProxy -- access to the storage
        :param cache_size: int -- Maximum size of query cache (default: {10})
        """
        self._storage = storage
        self._query_cache = LRUCache(capacity=cache_size)
        self.name = self._storage._table_name

        data = self._read()
        if data:
            self._last_id = max(i for i in data)
        else:
            self._last_id = 0

    def __str__(self):
        return '{}'.format(self.name)

    def process_records(self, func, cond=None, rids=None):
        """Helper function for processing all records specified by condition
        or IDs.
        
        The function passed as ``func`` has to be a callable. It's first
        argument will be the data currently in the database. It's second
        argument is the record ID of the currently processed record.

        :param func: type
        :param first: argument
        :param second: argument
        :param Keyword: Arguments
        :param cond: Query (Default value = None)
        :param rids: list (Default value = None)
        :returns: list -- the record IDs that were affected during processing

        """
        data = self._read()

        if rids is not None:
            # Processed record specified by id
            for rid in rids: 
                func(data, rid)

        else:
            # Collect affected rids
            rids = []

            # Processed records specified by condition 
            if rid in list(data):
                if cond(data[rid]):
                    func(data, rid)
                    rids.append(rid)

        self._write(data)

        return rids

    def clear_cache(self):
        """Clear the query cache.
        
        A simple helper that clears the internal query cache.


        """
        self._query_cache.clear()

    def _get_next_id(self):
        """Increment the ID used the last time and return it."""
        current_id = self._last_id + 1
        self._last_id = current_id

        return current_id

    def _read(self):
        """Reading access to the database.


        :returns: dict] -- all values

        """
        return self._storage.read()

    def _write(self, values):
        """Writing acccess to the database.

        :param values: dict

        """
        self._query_cache.clear()
        self._storage.write(values)

    def __len__(self):
        """Get the total number of records in a table"""
        return len(self._read())

    def all(self):
        """Get all records stored in the table.


        :returns: list] -- a list with all records.

        """
        return list(itervalues(self._read()))

    def __iter__(self):
        """Iterate over all records stored in the table.
        
        :yields: [listiterator[Record]] -- an iterator over all records.
        """
        for value in itervalues(self._read()):
            yield value

    def insert(self, record):
        """Insert a nwe record into the table.

        :param record: dict
        :returns: int] -- the inserted record's ID
        :raises ValueError: Record is not a dictionary

        """
        rid = self._get_next_id()

        if not isinstance(record, dict):
            raise ValueError('Record is not a dictionary')

        data = self._read()
        data[rid] = record
        self._write(data)

        return rid

    def insert_multiple(self, records):
        """Insert multiple records into the table.

        :param records: list
        :returns: list] -- a list containing the inserted records IDs

        """
        rids = []
        data = self._read()

        for record in records: 
            rid = self._get_next_id()
            rids.append(rid)

            data[rid] = record

        self._write(data)

        return rids

    def remove(self, cond=None, rids=None):
        """Remove all matching records.
        
        Keyword Arguments:
            cond {Query} -- the condition to check against (default: {None})
            rids {list} -- list of record IDs (default: {None})

        :param cond: Default value = None)
        :param rids: Default value = None)
        :returns: list] -- a list containing the removed record's ID

        """
        return self.process_records(
            lambda data, rid: data.pop(rid), cond, rids)

    def update(self, fields, cond=None, rids=None):
        """Update all matching records to have a given set of fields.

        :param fields: dict
        :param have: or a method that will update the records
        :param Keyword: Arguments
        :param cond: Query (Default value = None)
        :param rids: list (Default value = None)
        :returns: list] -- a list containing the updated record's ID

        """
        if callable(fields):
            return self.process_records(
                lambda data, rid: fields(data[rid]), cond, rids)
        else:
            return self.process_records(
                lambda data, rid: data[rid].update(fields), cond, rids)
    
    def purge(self):
        """Purge the table by removing all records"""
        self._storage.purge()
        self._last_id = 0

    def filter(self, cond):
        """Filter all records by matching condition

        :param cond: Query
        :returns: list[Record]] -- list of matching records

        """
        if cond in self._query_cache:
            return self._query_cache[cond][:]

        records = [record for record in self.all() if cond(record)]
        self._query_cache[cond] = records

        return records[:]

    def get(self, cond=None, rid=None):
        """Get exactly one record by matching condition.
        
        Keyword Arguments:
            cond {Query} -- the condition to check against (default: {None})
            rid {int} -- the record's ID  (default: {None})

        :param cond: Default value = None)
        :param rid: Default value = None)
        :returns: Record | None] -- the record or None

        """
        if rid is not None: 
            return self._read().get(rid, None)

        # Get record by condition
        for record in self.all():
            if cond(record):
                return record

    def count(self, cond):
        """Count all records matching a condition.

        :param cond: Query
        :returns: int] -- integer value of the count

        """
        return len(self.filter(cond))

    def contains(self, cond=None, rids=None):
        """Checks whether the table has an record matching a condition or ID.
        
        If ``rids`` is set, it checks if the db contains an record with one
        of the specified.
        
        Keyword Arguments:
            cond {Query} -- the condition (default: {None})
            rids {list} -- the record IDs (default: {None})

        :param cond: Default value = None)
        :param rids: Default value = None)
        :returns: Record | None] -- the record or None

        """
        if rids is not None:
            # Records specified by ID
            return any(self.get(rid=rid) for rid in rids)

        return self.get(cond) is not None

# Set the default table class
FlatFileDB.table_class = Table
