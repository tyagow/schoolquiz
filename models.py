from decimal import Decimal


class Teacher:
    def __init__(self, name):
        self.name = name
        self._class_rooms = []

    def __len__(self):
        return len(self._class_rooms)

    def add_class_rooms(self, *class_rooms):
        self._class_rooms.extend(class_rooms)


class Student:
    def __init__(self, name):
        self.name = name


class ClassRoom:

    def __init__(self):
        self._student_answers = {}
        self._assignments = {}
        self._students = []

    def __len__(self):
        return len(self._students)

    def add_students(self, *students):
        for student in students:
            self._students.append(student)
            self._student_answers[student.name] = []
            self._assignments[student.name] = []

    def assign_quiz(self, *quizes, student):
        self._assignments[student.name].extend(quizes)

    def get_quizes_for(self, student):
        return self._assignments[student.name]

    def submit_answer(self, answer, student):
        answers = self._student_answers[student.name]
        answers.append(answer)

    def get_grade_for(self, student):
        student_assigned_total_questions = sum(len(quiz) for quiz in self._assignments[student.name])
        grades = {}
        answers = self._student_answers[student.name]
        try:
            grades[student.name] = sum(answer.grade() for answer in answers) / student_assigned_total_questions
        except ZeroDivisionError:
            grades[student.name] = 0
        return grades


class Quiz:
    def __init__(self):
        self._questions = []

    def __len__(self):
        return len(self._questions)

    def add_questions(self, *questions):
        self._questions.extend(questions)


class Question:
    """
    title: represent the title of the Question
    _choices: represents all possible choices : List of strings [str,...]
    _correct_choice: index of the correct choice in _choices list
    """
    def __init__(self, *, title, correct_choice, choices):
        self._choices = choices
        self._title = title
        self._correct_choice = correct_choice

    def __len__(self):
        return len(self._choices)

    def add_choices(self, *choices):
        """Add choices or just one choice to the self._choices attribute list"""
        self._choices.extend(choices)

    def is_correct_choice(self, choice):
        return choice == self._correct_choice


class Answer:
    def __init__(self, question: Question, choice):
        self.question = question
        self.choice = choice

    def grade(self):
        return Decimal(1) if self.question.is_correct_choice(self.choice) else 0

