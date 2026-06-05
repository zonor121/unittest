import unittest

from netutils.ports import parse_port


class TestParsePortTypeErrors(unittest.TestCase):
    def test_raises_type_error_on_none(self):
        with self.assertRaises(TypeError):
            parse_port(None)

    def test_raises_type_error_on_list(self):
        with self.assertRaises(TypeError):
            parse_port([])

    def test_raises_type_error_on_dict(self):
        with self.assertRaises(TypeError):
            parse_port({})

    def test_raises_type_error_on_float(self):
        with self.assertRaises(TypeError):
            parse_port(3.14)

    def test_raises_type_error_on_bool_true(self):
        with self.assertRaises(TypeError):
            parse_port(True)

    def test_raises_type_error_on_bool_false(self):
        with self.assertRaises(TypeError):
            parse_port(False)


class TestParsePortValueErrors(unittest.TestCase):
    def test_raises_value_error_on_zero(self):
        with self.assertRaises(ValueError):
            parse_port(0)

    def test_raises_value_error_on_out_of_range_int(self):
        with self.assertRaises(ValueError):
            parse_port(65536)

    def test_raises_value_error_on_negative_int(self):
        with self.assertRaises(ValueError):
            parse_port(-1)

    def test_raises_value_error_on_empty_string(self):
        with self.assertRaises(ValueError):
            parse_port("")

    def test_raises_value_error_on_whitespace_string(self):
        with self.assertRaises(ValueError):
            parse_port("   ")

    def test_raises_value_error_on_non_digit_string(self):
        with self.assertRaises(ValueError):
            parse_port("abc")

    def test_raises_value_error_on_decimal_string(self):
        with self.assertRaises(ValueError):
            parse_port("1.5")


class TestParsePortValidInt(unittest.TestCase):
    def test_valid_port_min_boundary(self):
        self.assertEqual(parse_port(1), 1)

    def test_valid_port_max_boundary(self):
        self.assertEqual(parse_port(65535), 65535)

    def test_valid_port_typical(self):
        self.assertEqual(parse_port(80), 80)


class TestParsePortValidStr(unittest.TestCase):
    def test_valid_port_string_min(self):
        self.assertEqual(parse_port("1"), 1)

    def test_valid_port_string_max(self):
        self.assertEqual(parse_port("65535"), 65535)

    def test_valid_port_string_with_spaces(self):
        self.assertEqual(parse_port(" 80 "), 80)


class TestParsePortTableDriven(unittest.TestCase):
    def test_valid_ports_table(self):
        cases = [
            (1, 1),
            (65535, 65535),
            (80, 80),
            ("1", 1),
            ("65535", 65535),
            (" 443 ", 443),
        ]

        for value, expected in cases:
            with self.subTest(value=value, expected=expected):
                self.assertEqual(parse_port(value), expected)

    def test_invalid_ports_table(self):
        cases = [
            (None, TypeError),
            ([], TypeError),
            ({}, TypeError),
            (3.14, TypeError),
            (True, TypeError),
            (False, TypeError),
            (0, ValueError),
            (65536, ValueError),
            ("", ValueError),
            ("abc", ValueError),
        ]

        for value, exc_type in cases:
            with self.subTest(value=value):
                with self.assertRaises(exc_type):
                    parse_port(value)