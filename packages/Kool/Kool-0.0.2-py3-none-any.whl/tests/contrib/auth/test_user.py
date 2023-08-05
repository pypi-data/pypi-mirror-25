import os
import pytest

from kool.db.models import Model
from kool.db.flatfile import FlatFileDB
from kool.contrib.auth import User, Group, Permission
from kool.contrib.courses import Course
from kool.core.exceptions import PermissionNotFound

TESTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestUser(object):

    @classmethod
    def setup_class(cls):
        testdb = os.path.join(TESTS_DIR, 'fixtures')
        Model.db = FlatFileDB(path=testdb)
        cls.user = User(first_name='John', last_name='Doe', 
            email='john@doe.com', password='secretpwd')
        cls.user_id = cls.user.save()
        cls.group_id = Group('testers').save()
        cls.course_id = Course('Testers', cls.user_id).save()
        cls.permission_id = Permission(('add_testers', 'Add Testers'), cls.course_id).save()

    def test_str(self):
        assert str(self.user) == 'John Doe'
        assert self.user.short_name() == 'John'

    def test_check_password(self):
        wrong_pwd = 'wrongpwd'
        assert self.user.check_password(wrong_pwd) == False
        correct_pwd = 'secretpwd'
        assert self.user.check_password(correct_pwd) == True

    def test_add_group(self):
        self.user.add_group(self.group_id)
        assert len(self.user.groups) == 1

    def test_del_group(self):
        self.user.del_group(self.group_id)
        assert len(self.user.groups) == 0

    def test_add_permission(self):
        self.user.add_permission(self.permission_id)
        assert len(self.user.permissions) == 1

    def test_del_permission(self):
        self.user.del_permission(self.permission_id)
        assert len(self.user.permissions) == 0

    def test_has_perm(self):
        response_found = self.user.has_perm(self.permission_id)
        assert response_found == True
        
        with pytest.raises(PermissionNotFound):
            response_not_found = self.user.has_perm(100000)

