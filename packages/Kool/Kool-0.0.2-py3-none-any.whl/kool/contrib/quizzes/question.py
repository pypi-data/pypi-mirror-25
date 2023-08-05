from kool.db.models import Model, where, table
from .quiz import Quiz


class Question(Model):
    """Question model provides a set of questions for a quiz.
    
    Extends:
        Model

    """
    def __init__(self, description, quiz_id, **options):
        super().__init__()
        self.description = description

        quiz = table(Quiz)

        if quiz.get(where('_id') == str(quiz_id)):
            self.quiz_id = quiz_id
        else:
            raise ValueError('Quiz id not found!')

        self.choices = {}
        self.check = {}
        self.correct_answers = []
        self.answers = []

    def __str__(self):
        return '{}'.format(self.description)

    def __repr__(self):
        return '{}'.format(self.description)

    def add_choices(self, choices, correct_answers):
        """Adds a list of choices to a choices dictionary
        
        Keyword Arguments:
            choices {list} -- a list of choices (default: {[]})
            correct_answers {list} -- a list of correct answers (default: {[]})

        :param choices: 
        :param correct_answers: 

        """
        if not (isinstance(choices, list) and isinstance(correct_answers, list)):
            raise ValueError('Choices and correct answers must be provided in a list!')

        for index, choice in enumerate(choices, 1):
            self.choices[index] = choice
            for answer in correct_answers:
                if str(answer).lower() == str(choice).lower():
                    if not answer in self.correct_answers:
                        self.correct_answers.append((index, answer))

        self.update()
        
        return self.choices

    def add_answers(self, answer):
        """Adds an answer to a question.
        Only if it exists as one of the choice.

        :param answer: 

        """
        if int(answer) in self.choices:
            if not answer in self.answers:
                self.answers.append(answer)
        else:
            raise KeyError('Answer is not part of the choices!')

        self.update()

        return self.answers

    def check_answer(self):
        """Checks if provided answer is the correct one"""
        for answer in self.answers:
            for index, corr_answer in self.correct_answers:
                if str(answer) == str(index):
                    self.check[index] = 'Correct'
                else:
                    self.check[index] = 'Wrong'

        self.update()

        return self.check