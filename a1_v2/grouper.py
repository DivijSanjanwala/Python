"""CSC148 Assignment 1
=== CSC148 Winter 2020 ===
Department of Computer Science,
University of Toronto
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.
Authors: Misha Schwartz, Mario Badr, Christine Murad, Diane Horton, Sophia Huynh
and Jaisie Sin
All of the files in this directory and all subdirectories are:
Copyright (c) 2020 Misha Schwartz, Mario Badr, Christine Murad, Diane Horton,
Sophia Huynh and Jaisie Sin
=== Module Description ===
This file contains classes that define different algorithms for grouping
students according to chosen criteria and the group members' answers to survey
questions. This file also contain a classe that describes a group of students as
well as a grouping (a group of groups).
"""
from __future__ import annotations
import random
from typing import TYPE_CHECKING, List, Any
from course import sort_students

if TYPE_CHECKING:
    from survey import Survey
    from course import Course, Student


def slice_list(lst: List[Any], n: int) -> List[List[Any]]:
    """
    Return a list containing slices of <lst> in order. Each slice is a
    list of size <n> containing the next <n> elements in <lst>.
    The last slice may contain fewer than <n> elements in order to make sure
    that the returned list contains all elements in <lst>.
    === Precondition ===
    n <= len(lst)
    >>> slice_list([3, 4, 6, 2, 3], 2) == [[3, 4], [6, 2], [3]]
    True
    >>> slice_list(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [False]]
    True
    """
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i: i + n])
    return result


def windows(lst: List[Any], n: int) -> List[List[Any]]:
    """
    Return a list containing windows of <lst> in order. Each window is a list
    of size <n> containing the elements with index i through index i+<n> in the
    original list where i is the index of window in the returned list.
    === Precondition ===
    n <= len(lst)
    >>> windows([3, 4, 6, 2, 3], 2) == [[3, 4], [4, 6], [6, 2], [2, 3]]
    True
    >>> windows(['a', 1, 6.0, False], 3) == [['a', 1, 6.0], [1, 6.0, False]]
    True
    """

    if n == 0:
        return []

    i = 0
    new_list = []
    while (i + n) <= len(lst):
        new_list.append(lst[i: i + n])
        i += 1
    return new_list


class Grouper:
    """
    An abstract class representing a grouper used to create a grouping of
    students according to their answers to a survey.
    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def __init__(self, group_size: int) -> None:
        """
        Initialize a grouper that creates groups of size <group_size>
        === Precondition ===
        group_size > 1
        """
        self.group_size = group_size

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """ Return a grouping for all students in <course> using the questions
        in <survey> to create the grouping.
        """
        raise NotImplementedError


class AlphaGrouper(Grouper):
    """
    A grouper that groups students in a given course according to the
    alphabetical order of their names.
    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.
        The first group should contain the students in <course> whose names come
        first when sorted alphabetically, the second group should contain the
        next students in that order, etc.
        All groups in this grouping should have exactly self.group_size members
        except for the last group which may have fewer than self.group_size
        members if that is required to make sure all students in <course> are
        members of a group.
        Hint: the sort_students function might be useful
        """
        # Create a list of <course.students> sorted alphabetically by their name
        list_alpha = sort_students(course.students, 'name')

        # Use slice_list on the alphabetically sorted list
        # of size <self.group_size> to make sublists of students
        sliced_alpha = slice_list(list_alpha, self.group_size)

        # Make each of these sublists of students into groups and make a
        # grouping out of it
        grouping = Grouping()

        for sublist in sliced_alpha:
            subgroup = Group(sublist)
            grouping.add_group(subgroup)

        return grouping


class RandomGrouper(Grouper):
    """
    A grouper used to create a grouping of students by randomly assigning them
    to groups.
    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.
        Students should be assigned to groups randomly.
        All groups in this grouping should have exactly self.group_size members
        except for one group which may have fewer than self.group_size
        members if that is required to make sure all students in <course> are
        members of a group.
        """
        students = list(course.get_students())
        random.shuffle(students)

        sliced = slice_list(students, self.group_size)

        grouping = Grouping()

        for sublist in sliced:
            subgroup = Group(sublist)
            grouping.add_group(subgroup)

        return grouping


class GreedyGrouper(Grouper):
    """
    A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a greedy algorithm to create
    groups.
    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.
        Starting with a tuple of all students in <course> obtained by calling
        the <course>.get_students() method, create groups of students using the
        following algorithm:
        1. select the first student in the tuple that hasn't already been put
           into a group and put this student in a new group.
        2. select the student in the tuple that hasn't already been put into a
           group that, if added to the new group, would increase the group's
           score the most (or reduce it the least), add that student to the new
           group.
        3. repeat step 2 until there are N students in the new group where N is
           equal to self.group_size.
        4. repeat steps 1-3 until all students have been placed in a group.
        In step 2 above, use the <survey>.score_students method to determine
        the score of each group of students.
        The final group created may have fewer than N members if that is
        required to make sure all students in <course> are members of a group.
        """
        n = self.group_size
        students_tuple = course.get_students()

        # Make a start_list and to_add
        start_list = [students_tuple[0]]
        to_add = list(students_tuple[1:])

        grouping = Grouping()

        while len(to_add) > 0:
            # Find which index to remove from <to_add>. Pop the element at that
            # index in <to_add> and put it in <start_list>
            i = self._index_to_add(start_list, to_add, survey)
            start_list.append(to_add.pop(i))

            if len(start_list) == n:
                subgroup = Group(start_list)
                grouping.add_group(subgroup)
                start_list = []

                if len(to_add) != 0:
                    start_list = [to_add[0]]
                    to_add.pop(0)

        if len(start_list) != 0:
            subgroup = Group(start_list)
            grouping.add_group(subgroup)

        return grouping

    def _index_to_add(self, initial: List[Student],
                      to_add: List[Student],
                      survey: Survey
                      ) -> int:
        """
        Return the index of student in the list <to_add> that when added to
        <initial>, gives the highest score upon calling <survey.score_students>.
        == Precondition ==
        <initial> and <to_add> are non-empty lists.
        """
        n = self.group_size
        new_list = initial + [to_add[0]]
        best_score = survey.score_students(new_list)
        best = 0

        if len(initial) < n:
            for i in range(1, len(to_add)):
                new_list = initial + [to_add[i]]
                new_score = survey.score_students(new_list)
                if new_score > best_score:
                    best = i
                    best_score = new_score

        return best


class WindowGrouper(Grouper):
    """
    A grouper used to create a grouping of students according to their
    answers to a survey. This grouper uses a window search algorithm to create
    groups.
    === Public Attributes ===
    group_size: the ideal number of students that should be in each group
    === Representation Invariants ===
    group_size > 1
    """

    group_size: int

    def make_grouping(self, course: Course, survey: Survey) -> Grouping:
        """
        Return a grouping for all students in <course>.
        Starting with a tuple of all students in <course> obtained by calling
        the <course>.get_students() method, create groups of students using the
        following algorithm:
        1. Get the windows of the list of students who have not already been
           put in a group.
        2. For each window in order, calculate the current window's score as
           well as the score of the next window in the list. If the current
           window's score is greater than or equal to the next window's score,
           make a group out of the students in current window and start again at
           step 1. If the current window is the last window, compare it to the
           first window instead.
        In step 2 above, use the <survey>.score_students to determine the score
        of each window (list of students).
        In step 1 and 2 above, use the windows function to get the windows of
        the list of students.
        If there are any remaining students who have not been put in a group
        after repeating steps 1 and 2 above, put the remaining students into a
        new group.
        """
        n = self.group_size
        to_add = list(course.get_students())

        grouping = Grouping()

        while len(to_add) >= n:
            window_list = windows(to_add, n)
            current_score = survey.score_students(window_list[0])
            best_index = 0

            for i in range(1, len(window_list)):
                new_score = survey.score_students(window_list[i])
                if new_score > current_score:
                    best_index = i
                    current_score = new_score

            subgroup = Group(window_list[best_index])
            grouping.add_group(subgroup)

            for element in window_list[best_index]:
                to_add.remove(element)

        if len(to_add) != 0:
            subgroup = Group(to_add)
            grouping.add_group(subgroup)
            to_add.clear()

        return grouping


class Group:
    """
    A group of one or more students
    === Private Attributes ===
    _members: a list of unique students in this group
    === Representation Invariants ===
    No two students in _members have the same id
    """

    _members: List[Student]

    def __init__(self, members: List[Student]) -> None:
        """ Initialize a group with members <members> """
        self._members = members.copy()

    def __len__(self) -> int:
        """ Return the number of members in this group """
        return len(self._members)

    def __contains__(self, member: Student) -> bool:
        """
        Return True iff this group contains a member with the same id
        as <member>.
        """

        for members in self._members:
            if members.id == member.id:
                return True
        return False

    def __str__(self) -> str:
        """
        Return a string containing the names of all members in this group
        on a single line.
        You can choose the precise format of this string.
        """
        result = ""

        for student in self._members:
            result += str(student) + ", "

        # Only return result till 3rd last letter since the last two characters
        # ", " were added but are not required
        return result[0:-2]

    def get_members(self) -> List[Student]:
        """ Return a list of members in this group. This list should be a
        shallow copy of the self._members attribute.
        """
        return self._members.copy()


class Grouping:
    """
    A collection of groups
    === Private Attributes ===
    _groups: a list of Groups
    === Representation Invariants ===
    No group in _groups contains zero members
    No student appears in more than one group in _groups
    """

    _groups: List[Group]

    def __init__(self) -> None:
        """ Initialize a Grouping that contains zero groups """
        self._groups = []

    def __len__(self) -> int:
        """ Return the number of groups in this grouping """
        return len(self._groups)

    def __str__(self) -> str:
        """
        Return a multi-line string that includes the names of all of the members
        of all of the groups in <self>. Each line should contain the names
        of members for a single group.
        You can choose the precise format of this string.
        """
        result = ""
        for group in self._groups:
            result += str(group) + "\n"

        # The "/n" at the end should be removed
        return result[0:-1]

    def add_group(self, group: Group) -> bool:
        """
        Add <group> to this grouping and return True.
        Iff adding <group> to this grouping would violate a representation
        invariant don't add it and return False instead.
        """
        if len(group) == 0:
            return False

        potential_members = group.get_members()

        for group2 in self._groups:
            for students in group2.get_members():
                if students in potential_members:
                    return False

        self._groups.append(group)
        return True

    def get_groups(self) -> List[Group]:
        """ Return a list of all groups in this grouping.
        This list should be a shallow copy of the self._groups
        attribute.
        """
        return self._groups.copy()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'random',
                                                  'survey',
                                                  'course']})
