import unittest

from ghostpath.lessons import list_lessons, read_lesson


class LessonsTests(unittest.TestCase):
    def test_catalog_offline(self):
        report = list_lessons()
        self.assertTrue(report["offline_only"])
        self.assertEqual(len(report["lessons"]), 5)

    def test_not_found(self):
        with self.assertRaises(ValueError):
            read_lesson("not-present")
