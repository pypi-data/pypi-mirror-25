"""Defines the survey class."""


class Question(object):
    """An object representing a question.

    Arguments
    ---------
    question_str : string
        A string representing the question being asked.
    answers : list
        An array of string representing possible answers, in order.
    """

    def __init__(self, question_str, answers):
        self.question_str = question_str
        self.answers = answers


class Survey(object):
    """A survey object.

    Arguments
    ---------
    questions : list
        An array of Question objects.
    """

    def __init__(self, questions):
        self.questions = questions


class SurveySubmission(Survey):
    """A submitted survey with a budget.

    Arguments
    ---------
    questions : list
        An array of Question objects.
    budget : int
        A budget to spend on survey optimization, in US dollars.
    """

    def __init__(self, questions, budget):
        Survey.__init__(self, questions)
        self.budget = budget
