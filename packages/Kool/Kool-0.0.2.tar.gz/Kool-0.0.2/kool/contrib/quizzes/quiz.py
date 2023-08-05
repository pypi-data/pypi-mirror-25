from kool.db.models import Model, where, table
from kool.contrib.courses import Course


class Quiz(Model):
    """Quiz comprises of questions and answers"""

    def __init__(self, name, course_id, **options):
        super().__init__()
        self.name = name

        course = table(Course)

        if course.get(where('_id') == str(course_id)):
            self.course_id = course_id
        else:
            raise ValueError('Course id not found!')

        self.description = options.pop('description', None)

    def __str__(self):
        return '{}'.format(self.name)

    def __repr__(self):
        return '{}'.format(self.name)

    def add_question(self, description, choices=[], correct_answers=[]):
        """Adds a question to an existing quiz

        :param description: str
        :param Keyword: Arguments
        :param choices: list (Default value = [])
        :param correct_answers: list (Default value = [])

        """
        from .question import Question

        if self._id:
            q = Question(description, self._id)
            q.save()
            q.add_choices(choices, correct_answers)
        else:
            raise ValueError('Quiz has to be saved to add a question!')

    def questions(self):
        """Returns a list of all questions related to quiz"""
        from .question import Question
        question = table(Question)
        return question.filter(where('_id') == str(self._id))
