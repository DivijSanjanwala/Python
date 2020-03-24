import grouper
from course import Student, Course
from survey import MultipleChoiceQuestion, NumericQuestion, YesNoQuestion, \
    CheckboxQuestion, Answer, Survey
from criterion import HomogeneousCriterion, HeterogeneousCriterion, \
    LonelyMemberCriterion
from grouper import AlphaGrouper, RandomGrouper, GreedyGrouper, WindowGrouper, \
    Group, Grouping

# Create some Student objects
student1 = Student(1, "Sannat")
student2 = Student(2, "Divij")
student3 = Student(3, "Jay")
student4 = Student(4, "Roger")

# Create some course objects
course1 = Course("CSC148")
course2 = Course("CSC165")
course3 = Course("MAT137")

# Create some question objects
question1 = MultipleChoiceQuestion(1, "What is you favorite language",
                                   ['Python', 'JAVA', 'C++', 'Javascript'])
question2 = NumericQuestion(2, "Rate the difficulty of UofT", 1, 10)
question3 = YesNoQuestion(3, "Do you like university")
question4 = CheckboxQuestion(4, "What foods do you like",
                             ["Burger", "Salad", "Poutine", "Steak"])

# Create answer objects
answer1_1 = Answer('Python')
answer2_1 = Answer(5)
answer3_1 = Answer(True)
answer4_1 = Answer(['Salad', 'Poutine'])

answer1_2 = Answer('Javascript')
answer2_2 = Answer(7)
answer3_2 = Answer(True)
answer4_2 = Answer(['Burger', 'Poutine'])

# Create survey objects
survey1 = Survey([question1, question2, question3, question4])

student = Student(10, 'Divij')
student_1 = Student(20, 'Sannat')
student_2 = Student(30, 'Vaibhav')
student_3 = Student(40, 'Tanuj')

question = CheckboxQuestion(1, "What's your name?",
                            ['Sannat', 'Jay', 'Vaibhav', 'Divij'])

question_4 = MultipleChoiceQuestion(5, "What's your name?",
                                    ['Sannat', 'Jay', 'Vaibhav', 'Divij'])

question_2 = YesNoQuestion(3, "Do you like university")

question_3 = NumericQuestion(4, "What's your weight?", 10, 15)

student_list = [student, student_1, student_2, student_3]
course = Course('Computer Science')
course.enroll_students(student_list)
weight = 1

# List of answers
answer = Answer(True)
answer_1 = Answer(False)
answer_2 = Answer('Divij')
answer_3 = Answer(['Sannat'])
answer_4 = Answer('Divij')
answer_5 = Answer(11)
answer_6 = Answer(17)

# Setting answers to students for question_2
student.set_answer(question_2, answer)
student_1.set_answer(question_2, answer_1)
student_2.set_answer(question_2, answer)
student_3.set_answer(question_2, answer_1)

# Setting answers to students for question_4
student.set_answer(question_4, answer_2)
student_1.set_answer(question_4, answer_3)
student_2.set_answer(question_4, answer_4)
student_3.set_answer(question_4, answer_2)

# Setting criterion for survey questions

survey_x = Survey([question_2, question_4])
survey_x.set_criterion(HomogeneousCriterion(), question_2)
survey_x.set_criterion(HeterogeneousCriterion(), question_4)

# Finding similarities of student answers with answers of student_1:

# student = 1
# student_1 = 0 + 0 = 0
# student_2 = 1 + 1 = 2
# student_3 = 0 + 1 = 1


class TestStudent:
    def test___str__(self):
        assert str(student1) == "Sannat"

    def test_has_answer(self):
        assert not student1.has_answer(question1)

    def test_set_answer(self):
        student1.set_answer(question1, answer1_1)
        assert student1.has_answer(question1)

    def test_get_answer(self):
        assert student1.get_answer(question1) == answer1_1
        assert student1.get_answer(question2) is None
        student1.set_answer(question3, answer3_1)
        assert student1.get_answer(question3) == answer3_1


class TestCourse:
    def test_enroll_students_get_students_empty_list(self):
        assert course1.enroll_students([]) is None
        assert course1.get_students() == ()

    def test_enroll_students_get_students(self):
        course1.enroll_students([student1, student2])
        assert course1.get_students() == (student1, student2)

    def test_all_answered(self):
        # student1 already has answer for question1, question3
        # student2 has no answers as of yet
        assert not course1.all_answered(survey1)
        student1.set_answer(question2, answer2_1)
        student1.set_answer(question4, answer4_1)
        student2.set_answer(question1, answer1_2)
        student2.set_answer(question2, answer2_2)
        student2.set_answer(question3, answer3_2)
        student2.set_answer(question4, answer4_2)
        assert course1.all_answered(survey1)


class TestMultipleChoiceQuestion:
    def test___str__(self):
        assert isinstance(str(question1), str)

    def test_validate_answer(self):
        assert not question1.validate_answer(Answer(True))
        assert question1.validate_answer(answer1_1)
        assert not question1.validate_answer(Answer(''))

    def test_get_similarity_not_similar(self):
        assert question1.get_similarity(answer1_1, answer1_2) == 0.0

    def test_get_similarity_similar_but_different_instance(self):
        assert question1.get_similarity(answer1_1, Answer('Python')) == 1.0


class TestNumericQuestion:
    def test___str__(self):
        assert isinstance(str(question2), str)

    def test_validate_answer(self):
        assert not question2.validate_answer(Answer('1'))
        assert question2.validate_answer(answer2_1)

    def test_validate_answer_boundaries(self):
        assert question2.validate_answer(Answer(1))
        assert question2.validate_answer(Answer(10))

    def test_validate_answer_out_of_bound(self):
        assert not question2.validate_answer(Answer(15))
        assert not question2.validate_answer(Answer(-4))

    def test_get_similarity(self):
        similarity = question2.get_similarity(answer2_1, answer2_2)
        assert round(similarity, 2) == round(1 - 2 / 9, 2)


class TestYesNoQuestion:
    def test___str__(self):
        assert isinstance(str(question3), str)

    def test_validate_answer(self):
        assert question3.validate_answer(Answer(True))
        assert not question3.validate_answer(Answer(['True']))

    def test_get_similarity(self):
        assert question3.get_similarity(answer3_1, answer3_2) == 1.0
        assert question3.get_similarity(Answer(True), Answer(False)) == 0.0


class TestCheckboxQuestion:
    def test___str__(self):
        assert isinstance(str(question4), str)

    def test_validate_answer(self):
        assert question4.validate_answer(answer4_1)

    def test_validate_answer_some_overlap_but_fails(self):
        assert not question4.validate_answer(Answer(['Salad', 'Steak', 'N/A']))

    def test_get_similarity(self):
        similarity = question4.get_similarity(answer4_1, answer4_2)
        assert round(similarity, 2) == round(1 / 3, 2)
        similarity = question4.get_similarity(Answer(['Poutine']),
                                              Answer(['Steak']))
        assert similarity == 0


class TestAnswer:

    def test_is_valid(self) -> None:
        answer_x = Answer(['Jay', 'Divij'])
        answer_z = Answer(['Sannat'])
        assert answer_x.is_valid(question)
        assert answer_z.is_valid(question)

    def test_is_valid_2(self) -> None:
        assert answer.is_valid(question_2)

    def test_is_valid_3(self) -> None:
        assert answer.is_valid(question_3) is False
        assert answer_5.is_valid(question_3)

    def test_is_valid_4(self) -> None:
        assert answer_4.is_valid(question_4)


class TestSurvey:

    def test___len__(self) -> None:
        survey = Survey([question, question_2])
        questions = survey._questions
        assert len(questions) == 2
        survey_1 = Survey([])
        questions_1 = survey_1._questions
        assert len(questions_1) == 0

    def test__contains__(self) -> None:
        survey = Survey([question, question_2])
        questions = survey.get_questions()
        assert question in questions
        assert question_4 not in questions

    def test___str__(self) -> None:
        survey = Survey([question, question_2])
        assert "What's your name?" \
               "" \
               "What's your name"

    def test_get_questions(self) -> None:
        survey = Survey([question, question_2])
        assert survey.get_questions() == [question, question_2]

    def test__get_criterion(self) -> None:
        survey = Survey([question, question_2])
        criterion_1 = HeterogeneousCriterion()
        survey.set_criterion(criterion_1, question)
        assert survey._get_criterion(question) == criterion_1
        assert survey._get_criterion(question_2) == survey._default_criterion

    def test_get_weight(self) -> None:
        survey = Survey([question, question_2])
        survey.set_weight(10, question)
        assert survey._get_weight(question) == 10
        assert survey._get_weight(question_2) == survey._default_weight

    def test_set_weight(self) -> None:
        survey = Survey([question, question_2])
        survey.set_weight(weight, question)
        assert survey._get_weight(question) == weight

    def test_set_criterion(self) -> None:
        survey = Survey([question, question_2])
        criterion = HeterogeneousCriterion()
        assert survey.set_criterion(criterion, question)
        assert survey._get_criterion(question) == criterion

    def test_score_grouping(self) -> None:
        survey = Survey([question, question_2])
        grouping = Grouping()
        group = Group([])
        students = [student, student_1]
        group_1 = Group(students)
        grouping.add_group(group)
        assert survey.score_grouping(grouping) == 0


class TestHomogeneousCriterion:

    def test_score_answers_TestHomogeneousCriterion(self) -> None:
        criterion = HomogeneousCriterion()
        question_object = question
        answers = [Answer(True), Answer('Divij'), Answer('Sannat')]
        assert not answers[0].is_valid(question_object)
        # assert criterion.score_answers(question_object, answers) == \
        #        'This answer is invalid'

    def test_score_answers_TestHomogeneousCriterion_valid(self) -> None:
        criterion_1 = HomogeneousCriterion()
        answers = [Answer(['Divij']), Answer(['Sannat']), Answer(['Divij'])]
        assert round(criterion_1.score_answers(question, answers), 2) == 0.33


class TestHeterogeneousCriterion:

    def test_score_answers_Test_Heterogeneous_Criterion(self) -> None:
        criterion = HeterogeneousCriterion()
        answers = [Answer(True), Answer(['Divij']), Answer(['Sannat'])]
        assert not answers[0].is_valid(question)
        # assert criterion.score_answers(question, answers)
        # is InvalidAnswerError

    def test_score_answers_Test_Heterogeneous_Criterion_valid(self) -> None:
        criterion_1 = HeterogeneousCriterion()
        answers = [Answer(['Divij']), Answer(['Sannat']), Answer(['Divij'])]
        assert round(criterion_1.score_answers(question, answers), 2) == 0.67


class TestLonelyMemberCriterion:

    def test_score_answers_Test_LonelyMemberCriterion(self) -> None:
        criterion_1 = LonelyMemberCriterion()
        answers = [Answer(['Divij']), Answer(['Sannat']),
                   Answer(['Divij']), Answer(['Divij'])]
        assert round(criterion_1.score_answers(question, answers), 2) == 0.0

    def test_score_answers_Test_LonelyMemberCriterion_(self) -> None:
        criterion_1 = LonelyMemberCriterion()
        answers = [Answer(['Divij'])]
        assert round(criterion_1.score_answers(question, answers), 2) == 0.0


def test_slice_list() -> None:
    to_be_sliced = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert grouper.slice_list(to_be_sliced, 2) == [[1, 2], [3, 4], [5, 6],
                                                   [7, 8], [9, 10]]
    assert grouper.slice_list(to_be_sliced, 3) == [[1, 2, 3], [4, 5, 6],
                                                   [7, 8, 9], [10]]
    assert grouper.slice_list(to_be_sliced, 5) == [[1, 2, 3, 4, 5],
                                                   [6, 7, 8, 9, 10]]


def test_windows() -> None:
    to_be_sliced = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert grouper.windows(to_be_sliced, 4) == [[1, 2, 3, 4], [2, 3, 4, 5],
                                                [3, 4, 5, 6], [4, 5, 6, 7],
                                                [5, 6, 7, 8], [6, 7, 8, 9], [7, 8, 9, 10]]
    assert grouper.windows(to_be_sliced, 1) == [[1], [2], [3], [4], [5],
                                                [6], [7], [8], [9], [10]]
    assert grouper.windows(to_be_sliced, 3) == [[1, 2, 3], [2, 3, 4], [3, 4, 5],
                                                [4, 5, 6], [5, 6, 7], [6, 7, 8],
                                                [7, 8, 9], [8, 9, 10]]


class TestAlphaGrouper:

    def test_init(self) -> None:
        alpha = grouper.AlphaGrouper(1)
        assert alpha.group_size == 1

    def test_make_grouping(self) -> None:
        alpha = grouper.AlphaGrouper(2)
        survey = Survey([question, question_2])  # CheckBox and YesNoQuestion
        grouping = alpha.make_grouping(course, survey)
        groups = grouping.get_groups()

        assert groups[0].get_members() == [student, student_1]
        assert groups[1].get_members() == [student_3, student_2]


# class TestRandomGrouper:
#     pass


class TestGreedyGrouper:

    def test_init(self) -> None:
        greedy = grouper.GreedyGrouper(2)
        assert greedy.group_size == 2

    def test_make_grouping(self) -> None:
        greedy = grouper.GreedyGrouper(2)
        grouping = greedy.make_grouping(course, survey_x)
        groups = grouping.get_groups()

        assert groups[0].get_members() == [student, student_2]
        assert groups[1].get_members() == [student_1, student_3]


class TestWindowGrouper:

    def test_init(self) -> None:
        window = grouper.WindowGrouper(2)
        assert window.group_size == 2

    def test_make_grouping(self) -> None:

        window = grouper.WindowGrouper(2)
        grouping = window.make_grouping(course, survey_x)
        groups = grouping.get_groups()

        assert groups[0].get_members() == [student, student_1]
        assert groups[1].get_members() == [student_2, student_3]


class TestGroup:

    def test_group___len__(self) -> None:

        group = grouper.Group([])
        assert group.__len__() == 0
        group_1 = grouper.Group([student_1, student_3])
        assert group_1.__len__() == 2

    def test_group___contains__(self) -> None:

        group = grouper.Group([])
        group_1 = grouper.Group([student_1, student_2])
        assert not group.__contains__(student_1)
        assert group_1.__contains__(student_1)

    def test_group___str__(self) -> None:

        group = grouper.Group([])
        group_1 = grouper.Group([student, student_1])
        string = group.__str__()
        string_1 = group_1.__str__()
        assert 'Vaibhav' not in string
        assert 'Tanuj' not in string_1
        assert 'Divij' not in string
        assert 'Sannat' in string_1

    def test_group_get_members(self) -> None:

        group = grouper.Group([student, student_1])
        members = group.get_members()
        assert members is not group

        for member in range(len(members)):
            assert members[member] is group._members[member]


class TestGrouping:

    def test_grouping___len__(self) -> None:
        grouping = grouper.Grouping()
        assert len(grouping) == 0
        group = grouper.Group([student, student_1])
        group_1 = grouper.Group([student_3, student_2])
        grouping.add_group(group)
        grouping.add_group(group_1)
        assert len(grouping) == 2

    def test_grouping___str__(self) -> None:

        grouping = grouper.Grouping()
        group = grouper.Group([student, student_1])
        group_1 = grouper.Group([student_2])
        group_2 = grouper.Group([student_3])
        grouping.add_group(group)
        grouping.add_group(group_2)

        assert 'Divij' in str(grouping)
        assert 'Sannat' in str(grouping)
        assert 'Vaibhav' not in str(grouping)
        assert 'Tanuj' in str(grouping)

    def test_grouping_add_group(self) -> None:

        grouping = grouper.Grouping()
        assert len(grouping) == 0
        group = grouper.Group([student, student_1])
        group_1 = grouper.Group([])
        assert grouping.add_group(group)
        assert not grouping.add_group(group_1)

    def test_grouping_get_groups(self) -> None:

        grouping = grouper.Grouping()
        group = grouper.Group([student, student_1])
        group_1 = grouper.Group([student_2])
        grouping.add_group(group)
        grouping.add_group(group_1)

        shallow_copy = grouping.get_groups()

        for group in shallow_copy:
            assert group is not grouping._groups
            assert group in grouping._groups


if __name__ == "__main__":
    import pytest
    pytest.main(['tests.py'])
