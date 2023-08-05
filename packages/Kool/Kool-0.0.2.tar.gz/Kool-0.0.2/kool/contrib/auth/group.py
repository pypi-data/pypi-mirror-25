from kool.db.models import Model, where, table
from .permission import Permission


class Group(Model):
    """Groups are used to cluster similar users.
    
    Extends:
        Model

    """

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.permissions = []

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '{}'.format(self.name)

    def add_permission(self, perm_id):
        """Receives a permission id, queries it and
        if it exists, adds it to list of permissions of
        a  given group

        :param perm_id: 

        """
        permission = table(Permission)

        if permission.get(where('_id') == str(perm_id)):
            if not perm_id in self.permissions:
                self.permissions.append(perm_id)
        else:
            raise ValueError('Topic id not found!')
        
        self.update()
        
        return self.permissions

    def del_permission(self, perm_id):
        """Receives a permission id and deletes it from
        a list of permissions for a given group

        :param perm_id: 

        """
        if perm_id in self.permissions:
            self.permissions.remove(perm_id)
        
        self.update()

        return self.permissions