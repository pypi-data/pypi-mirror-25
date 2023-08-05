from kool.db.models import Model, where, table
from kool.contrib.courses import Course


class Permission(Model):
    """Permissions are used to determine actions permitted on a course
    by a user or group
    
    Extends:
        Model

    """
    PERMISSIONS = ('add', 'edit', 'delete')

    def __init__(self, perm, course_id):
        super().__init__()
        
        if not isinstance(perm, tuple):
            raise ValueError('Permission has to be a tuple!')

        course = table(Course)

        if course.get(where('_id') == str(course_id)):
            self.course_id = course_id
        else:
            raise ValueError('Course id not found!')

        if perm:
            self.codename = perm[0] if perm[0].split('_')[0] in self.PERMISSIONS else None
            self.name = perm[1] if perm else None

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '{}'.format(self.name)
