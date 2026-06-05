import unittest
from unittest.mock import patch

from app.user_profile import wait_until_ready


class TestWaitUntilReadyFast(unittest.TestCase):
    def test_ready_after_two_polls(self):
        states = iter(["pending", "pending", "ready"])

        def check():
            return next(states)

        with (
            patch("app.user_profile.time.sleep") as mocked_sleep,
            patch("app.user_profile.time.monotonic", side_effect=[0.00, 0.00, 0.10, 0.20]),
        ):
            result = wait_until_ready(check, timeout=0.30, interval=0.10)

        self.assertTrue(result)
        self.assertEqual(mocked_sleep.call_count, 2)

    def test_timeout(self):
        with (
            patch("app.user_profile.time.sleep") as mocked_sleep,
            patch("app.user_profile.time.monotonic", side_effect=[0.00, 0.00, 0.10, 0.20, 0.31]),
        ):
            result = wait_until_ready(lambda: "pending", timeout=0.30, interval=0.10)

        self.assertFalse(result)
        self.assertEqual(mocked_sleep.call_count, 3)