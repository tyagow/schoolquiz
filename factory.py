from models import Question, ClassRoom, Quiz, Student, Teacher


class QuestionBuilder:

    @staticmethod
    def create_question(title="1+1", correct_choice=1, choices=['0', '2', '5']):
        return Question(title=title, correct_choice=correct_choice, choices=choices)


class ClassRoomBuilder:

    @staticmethod
    def create_classroom() -> ClassRoom:
        return ClassRoom()


class QuizBuilder:

    @staticmethod
    def create_quiz() -> Quiz:
        return Quiz()


class StudentBuilder:

    @staticmethod
    def create_student(name="Default Student") -> Student:
        return Student(name=name)


class TeacherBuilder(object):

    @staticmethod
    def create_teacher(name="Default Teacher") -> Teacher:
        return Teacher(name=name)

