import os
import unittest
import importlib.util

from config_parsing import parse_port, parse_bool, parse_csv


class TestValidParsing(unittest.TestCase):
    def test_valid_ports(self):
        cases = [
            ("1", 1),
            (" 80 ", 80),
            ("\t65535\n", 65535),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                self.assertEqual(parse_port(raw), expected)

    def test_valid_bools(self):
        cases = [
            ("true", True),
            (" FALSE ", False),
            ("1", True),
            ("0", False),
            (" Yes ", True),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                self.assertEqual(parse_bool(raw), expected)

    def test_valid_csv(self):
        cases = [
            ("a, b, c", ["a", "b", "c"]),
            (" 1 , 2 , 3 ", ["1", "2", "3"]),
            ("x,,y", ["x", "y"]),
            ("   ", []),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw, expected=expected):
                self.assertEqual(parse_csv(raw), expected)


class TestInvalidParsing(unittest.TestCase):
    def test_invalid_ports(self):
        cases = [
            ("", ValueError, "valid decimal integer"),
            ("0", ValueError, "out of range"),
            ("65536", ValueError, "out of range"),
            (None, TypeError, "must be str"),
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_port(raw)

    def test_invalid_bools(self):
        cases = [
            ("maybe", ValueError, "invalid boolean literal"),
            (123, TypeError, "must be str"),
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_bool(raw)

    def test_invalid_csv(self):
        cases = [
            (None, TypeError, "must be str"),
        ]
        for raw, exc_type, msg_part in cases:
            with self.subTest(raw=raw, exc=exc_type.__name__):
                with self.assertRaisesRegex(exc_type, msg_part):
                    parse_csv(raw)


RUN_SLOW = os.environ.get("RUN_SLOW") == "1"


@unittest.skipUnless(RUN_SLOW, "set RUN_SLOW=1 to enable extended parsing tests")
class TestExtendedParsing(unittest.TestCase):
    def test_extended_ports(self):
        cases = [
            ("00080", 80),
            ("00001", 1),
            ("00", ValueError),
            ("-1", ValueError),
            ("99999", ValueError),
            ("10000", 10000),
            ("5000", 5000),
            ("22", 22),
            ("443", 443),
            ("8080", 8080),
            ("3000", 3000),
            ("8000", 8000),
            ("9000", 9000),
            ("100", 100),
            ("65534", 65534),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                if expected is ValueError:
                    with self.assertRaises(ValueError):
                        parse_port(raw)
                else:
                    self.assertEqual(parse_port(raw), expected)


yaml_spec = importlib.util.find_spec("yaml")


@unittest.skipUnless(yaml_spec is not None, "requires PyYAML: pip install pyyaml")
class TestOptionalDependencyParsing(unittest.TestCase):
    def test_yaml_parsing(self):
        import yaml
        data = yaml.safe_load("port: 80\n")
        self.assertEqual(data["port"], 80)