from .flatfile import FlatFileDB, Query
from kool.utils import camel_to_snake, now


class Model(object):
    db = None  # database

    def __init__(self, * args, ** kwargs):
        """
        Model provides save, delete, purge operations to every
        class that inherits it.
        """
        
        # Get class name, so as to set the table name
        cls_name = self.__class__.__name__
        table_name = camel_to_snake(cls_name)
        self._table = Model.db.create_table(name=table_name)
        self.last_modified = None
        self.date_created = None
        self._id = None

    def save(self, * args, ** kwargs):
        """
        Saves current object to database.
        It also updates the `last_modified` and `date_created` fields.
        """
        data = {}
        self.last_modified = '{}'.format(now())
        if not self.date_created:
            self.date_created = '{}'.format(now())
        
        # Get objects dict
        data = self.props()

        if data:
            # Creates a new instance
            self._id = self._table.insert(data)

        return self._id

    def update(self, * args, ** kwargs):
        """
        Update method provides a way of updating the values of an object.
        """
        data = {}
        self.last_modified = '{}'.format(now())
        if not self.date_created:
            self.date_created = '{}'.format(now())
        
        # Get objects dict
        data = self.props()

        # Fetch exising object
        obj = self._table.get(rid=self._id) if self._id else None
        
        if obj and data:
            # Updates an existing instance
            ids = self._table.update(data, rids=[self._id])
            self._id = ids[0]
        
        return self._id

    def delete(self, cond=None, rids=None, * args):
        rids = []

        rids = ([self._id,] if self._id else []) or rids or list(args)
        if rids:
            self._table.remove(cond=cond, rids=rids)
        else:
            raise ValueError('Record must be saved to delete')

    def purge(self, confirm=False):
        """
        Truncates the table. Operation is irreversible.
        
        Keyword Arguments:
            confirm {bool} -- user confirmation (default: {False})
        """
        if confirm:
            self._table.purge()
        else:
            raise ValueError('Confirm argument has to be set true')

    def props(self):
        """Converts object to dictionary"""
        return dict(
            (key, value) 
            for (key, value) in self.__dict__.items() 
            if not (key.startswith('_') or key.startswith('__')))

    def __getattr__(self, name):
        """
        Forward all unknown attribute calls to the underlying standard table.
        """
        return getattr(self._table, name)


# Instantiate database
Model.db = FlatFileDB()


def where(key):
    return Query()[key]


def table(cls):
    """Returns a table object given a class"""
    cls_name = cls.__name__
    table_name = camel_to_snake(cls_name)
    return Model().db.table(table_name)
