import os
import pytest

from kool.db.models import Model
from kool.db.flatfile import FlatFileDB
from kool.contrib.auth import User
from kool.contrib.courses import Course
from kool.contrib.quizzes import Quiz, Question

TESTS_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestQuestion(object):

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
        cls.question = Question('favourite pet?', cls.quiz_id)
        cls.question_id = cls.question.save()    

    def test_add_choices(self):
        self.question.add_choices(choices=['cat', 'dog', 'bird'], correct_answers=['dog'])
        assert self.question.choices == {1: 'cat', 2: 'dog', 3: 'bird'}
        assert self.question.correct_answers == [(2, 'dog')]

    def test_add_answers(self):
        self.question.add_answers(2)
        assert isinstance(self.question.answers, list)
        assert self.question.answers[0] == 2

        with pytest.raises(KeyError):
            self.question.add_answers(4)

    def test_check_answer(self):
        response = self.question.check_answer()
        assert response == {2: 'Correct'}



