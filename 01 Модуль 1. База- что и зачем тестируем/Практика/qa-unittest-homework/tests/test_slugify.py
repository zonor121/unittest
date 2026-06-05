import unittest

from qautils.slugify import slugify


class TestSlugify(unittest.TestCase):
    def test_examples_from_specification(self):
        cases = [
            ("Hello, World!", "hello-world"),
            ("  multiple   spaces  ", "multiple-spaces"),
            ("Already_Slug", "already-slug"),
            ("---A---B---", "a-b"),
            ("!!!", ""),
        ]

        for text, expected in cases:
            with self.subTest(text=text):
                self.assertEqual(slugify(text), expected)

    def test_keeps_digits_and_latin_letters(self):
        self.assertEqual(slugify("Release 2026 v2"), "release-2026-v2")

    def test_collapses_mixed_separators(self):
        self.assertEqual(slugify("one__  two---three"), "one-two-three")


if __name__ == "__main__":
    unittest.main()
