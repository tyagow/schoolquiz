from collections import namedtuple
from decimal import Decimal

import pytest

from factory import QuestionBuilder, ClassRoomBuilder, QuizBuilder, StudentBuilder, TeacherBuilder
from models import Question, ClassRoom, Student, Answer, Teacher, Quiz

"""
There​ ​ are​ ​ Teachers | There​ ​ are​ ​ Students
Students​ ​ are​ ​ in​ ​ classes​ ​ that​ ​ teachers​ ​ teach
Teachers​ ​ can​ ​ create​ ​ multiple​ ​ quizzes​ ​ with​ ​ many​ ​ questions​ ​ (each​ ​ question​ ​ is​ ​ multiple​ ​ choice)
Teachers​ ​ can​ ​ assign​ ​ quizzes​ ​ to​ ​ students
Students​ ​ solve/answer​ ​ questions​ ​ to​ ​ complete​ ​ the​ ​ quiz,​ ​ but​ ​ they​ ​ don't​ ​ have​ ​ to​ ​ complete​ ​ it​ ​ at
once.​ ​ (Partial​ ​ submissions​ ​ can​ ​ be​ ​ made).
Quizzes​ ​ need​ ​ to​ ​ get​ ​ graded
For​ ​ each​ ​ teacher,​ ​ they​ ​ can​ ​ calculate​ ​ each​ ​ student's​ ​ total​ ​ grade​ ​ accumulated​ ​ over​ ​ a ​ ​ semester
for​ ​ their​ ​ classes

Assumptions:
    
    - Each ClassRoom will contain N Students
    - Each Quiz will contain N Questions 
    - Each Question will contain N Choices
    - Each Question must know correct choice
    - Question requires to be instantiated: 
                        - title, (string)
                        - correct_choice (int | index of choices list)
                        - choices  (list of strings)
    - Each Student must have a name attribute
    - For simplicity i assume that are no repeated Students name or we would need and id attribute
    - Student name will be used as index/id
"""


def setup_test() -> namedtuple:
    """
    :return: an instance of SetupTest with one student assign with one quiz in one classroom. Quiz has one question
    """
    SetupTest = namedtuple('SetupTest', ['class_room', 'student', 'quiz', 'question'])

    student = StudentBuilder.create_student()
    quiz = QuizBuilder.create_quiz()
    question = QuestionBuilder.create_question()
    quiz.add_questions(question)
    class_room = ClassRoomBuilder.create_classroom()
    class_room.add_students(student)
    class_room.assign_quiz(quiz, student=student)

    return SetupTest(class_room=class_room, student=student, quiz=quiz, question=question)


def test_classroom_creation():
    class_room = ClassRoomBuilder.create_classroom()
    assert isinstance(class_room, ClassRoom)


@pytest.mark.parametrize(
    'students',
    [
        [StudentBuilder.create_student()],
        [StudentBuilder.create_student() for _ in range(10)]
    ]
)
def test_classroom_can_add_students(students):
    """Students​ ​ are​ ​ in​ ​ classes​ ​ that​ ​ teachers​ ​ teach"""
    class_room = ClassRoomBuilder.create_classroom()
    class_room.add_students(*students)
    assert len(class_room) == len(students)


@pytest.mark.parametrize(
    'questions',
    [
        [QuestionBuilder.create_question()],
        [QuestionBuilder.create_question() for _ in range(10)]
    ]
)
def test_each_quiz_can_have_multiple_questions(questions):
    """quizzes with many questions"""
    quiz = QuizBuilder.create_quiz()
    quiz.add_questions(*questions)
    assert len(quiz) == len(questions)


def test_question_raises_error_if_any_required_param_not_passed():
    """
    Question requires to be instantiated:
                        - title, (string)
                        - correct_choice (int | index of choices list)
                        - choices  (list of strings)

    """
    with pytest.raises(TypeError):
        Question()
        Question(title="test title")
        Question(title="test title", correct_choice=1)
        Question(title="test title", choices=["2", "4"])
    question = QuestionBuilder.create_question()
    assert hasattr(question, '_title')
    assert hasattr(question, '_correct_choice')
    assert hasattr(question, '_choices')


def test_teacher_can_assign_quizzes_to_students():
    """
    Teachers​ ​ can​ ​ assign​ ​ quizzes​ ​ to​ ​ students
    """
    student = StudentBuilder.create_student()
    class_room = ClassRoomBuilder.create_classroom()
    class_room.add_students(student)
    quiz = QuizBuilder.create_quiz()
    questions = [QuestionBuilder.create_question(title="2+2?"), QuestionBuilder.create_question(title="2+4?")]
    quiz.add_questions(questions)
    class_room.assign_quiz(quiz, student=student)
    student_quizes = class_room.get_quizes_for(student)
    assert quiz in student_quizes


def test_student_has_name_attribute():
    """
    Student must have a name atribute

    """
    with pytest.raises(TypeError):
        Student()


"""
Students solve/answer questions to complete the quiz,
but they don't have to complete it at
"""


def test_quiz_save_partial_answers_from_student():
    """
    A Student must be able to submit answers to quiz
    """
    class_room, student, quiz, question = setup_test()
    question_two = QuestionBuilder.create_question(title="3x3")
    quiz.add_questions(question_two)
    answer = Answer(question, question._correct_choice)
    class_room.submit_answer(answer, student)
    assert class_room.get_grade_for(student) == {student.name: Decimal('0.5')}


def test_answer_grade_retuns_1_when_correct():
    """
    Assumption: when an answer is correct it should return 1 else 0
    :return:
    """
    question = QuestionBuilder.create_question()
    answer = Answer(question, question._correct_choice)
    assert answer.grade() == Decimal(1)


@pytest.mark.parametrize(
    'class_rooms',
    [
        [ClassRoomBuilder.create_classroom()],
        [ClassRoomBuilder.create_classroom() for _ in range(10)]
    ]
)
def test_teacher_can_add_class_room(class_rooms):
    """Teacher can teach multiple class_rooms"""
    teacher = TeacherBuilder.create_teacher()
    teacher.add_class_rooms(*class_rooms)
    assert len(class_rooms) == len(teacher)


def test_integration():
    teacher = TeacherBuilder.create_teacher()
    student_one = Student(name='John')
    class_room = ClassRoom()
    teacher.add_class_rooms(class_room)
    class_room.add_students(student_one)
    quiz = Quiz()
    one_plus_one = Question(title='1+1', correct_choice=1, choices=['1', '2', '4'])
    two_plus_two = Question(title='2+2', correct_choice=0, choices=['4', '5'])
    quiz.add_questions(one_plus_one, two_plus_two)
    class_room.assign_quiz(quiz, student=student_one)
    assert class_room.get_grade_for(student=student_one) == {'John': Decimal('0')}
    class_room.submit_answer(answer=Answer(one_plus_one, 1), student=student_one)
    assert class_room.get_grade_for(student=student_one) == {'John': Decimal('0.5')}
    class_room.submit_answer(answer=Answer(two_plus_two, 0), student=student_one)
    assert class_room.get_grade_for(student=student_one) == {'John': Decimal('1')}
    student_two = Student(name='Carl')
    class_room.add_students(student_two)
    class_room.assign_quiz(quiz, student=student_two)
    assert class_room.get_grade_for(student=student_two) == {'Carl': Decimal('0')}
    class_room.submit_answer(answer=Answer(one_plus_one, 1), student=student_two)
    assert class_room.get_grade_for(student=student_two) == {'Carl': Decimal('0.5')}
    class_room.submit_answer(answer=Answer(two_plus_two, 0), student=student_two)
    assert class_room.get_grade_for(student=student_two) == {'Carl': Decimal('1')}