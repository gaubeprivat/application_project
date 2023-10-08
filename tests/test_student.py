"""
Modul: test_student
Author: Benjamin Gaube
Date: 2023-10-08
"""  # TODO

import os
import unittest
from typing import Tuple

from src.main import FILENAME
from test_main import TestModul
from src.student import Student


class TestStaticmethod(TestModul):
    def test_extract_grades(self):
        grades = Student.extract_grades(os.path.join(self.unpacked_directory, 'StudentGrades.txt'))
        self.assertNotEqual(grades['mid1']['S1'], 79)
        self.assertEqual(grades['mid1']['S1'], 78)
        self.assertEqual(grades['mid2']['S5'], 77)
        self.assertEqual(grades['final']['S10'], 116)


class TestStudentModul(TestModul):

    all_grades = Student.extract_grades(os.path.join(TestStaticmethod.main_zip_path, FILENAME, 'StudentGrades.txt'))

    def setUp(self):
        super().setUp()
        self.students_directory = os.path.join(self.unpacked_directory, 'Data.zip')

    @classmethod
    def personal_grades(cls, student_id: str) -> Tuple[int, int, int]:
        """
        Reorganize the grades of a specific student. This methode is inspired
        by the syntax used in student_factory of the main modul.
        """  # TODO: Docstring anpassen

        term_keys = [key for key in cls.all_grades]
        personal_grades = (
            cls.all_grades[term_keys[0]][student_id],
            cls.all_grades[term_keys[1]][student_id],
            cls.all_grades[term_keys[2]][student_id]
        )

        return personal_grades

    def test_constructor(self):
        some_student = Student(self.students_directory, 'S1', TestStudentModul.personal_grades('S1'))
        self.assertNotEqual(some_student.student_id, 'S2')
        self.assertEqual(some_student.student_id, 'S1')
        self.assertEqual(some_student.grades[0], 78)
        self.assertEqual(some_student.grades[1], 82)
        self.assertEqual(some_student.grades[2], 182)
        self.assertEqual(some_student.path, os.path.join(self.students_directory, 'S1'))

        some_other_student = Student(self.students_directory, 'S7', TestStudentModul.personal_grades('S7'))
        self.assertEqual(some_other_student.grades[1], 33)


if __name__ == '__main__':
    unittest.main()