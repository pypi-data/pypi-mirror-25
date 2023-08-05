import os
import pytest

from kool.db.models import Model
from kool.db.flatfile import FlatFileDB
from kool.contrib.auth import User
from kool.contrib.courses import Course
from kool.contrib.quizzes import Quiz, Question

TESTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestQuiz(object):

    @classmethod
    def setup_class(cls):
        testdb = os.path.join(TESTS_DIR, 'fixtures')
        Model.db = FlatFileDB(path=testdb)
        cls.user = User(first_name='John', last_name='Doe', 
            email='john@doe.com', password='secretpwd')
        cls.user_id = cls.user.save()
        cls.course_id = Course('Testers', cls.user_id).save()
        cls.quiz = Quiz('quiz test', cls.course_id)
        cls.quiz_id = cls.quiz.save()

    def test_add_question(self):
        self.quiz.add_question('favourite pet?', 
            choices=['cat', 'dog', 'bird'], correct_answers=['dog'])

        assert self.quiz.questions()[0]['choices'] == "{1: 'cat', 2: 'dog', 3: 'bird'}"
        assert self.quiz.questions()[0]['correct_answers'] == "[(2, 'dog')]"
