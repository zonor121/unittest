import unittest

from qaututils.slugify import slugify


class TestSlugify(unittest.TestCase):
    def test_slugify_cases(self):
        cases = [
            ("Hello, World!", "hello-world"),
            (" multiple spaces ", "multiple-spaces"),
            ("Already_Slug", "already-slug"),
            ("---A---B---", "a-b"),
            ("!!!", ""),
            ("", ""),
            ("   ", ""),
        ]

        for text, expected in cases:
            with self.subTest(text=text, expected=expected):
                self.assertEqual(slugify(text), expected)