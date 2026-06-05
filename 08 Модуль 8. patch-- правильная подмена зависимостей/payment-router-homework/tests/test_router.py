import unittest
from unittest.mock import Mock, patch

from payment.router import choose_payment_mode, charge_order


class TestChoosePaymentMode(unittest.TestCase):
    def test_prod_mode_by_default_when_no_env_vars(self):
        with patch.dict("os.environ", {}, clear=True):
            result = choose_payment_mode()
        self.assertEqual(result, "gateway")

    def test_sandbox_mode_when_payment_env_is_test(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = choose_payment_mode()
        self.assertEqual(result, "sandbox")

    def test_sandbox_mode_when_payment_env_is_dev(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "dev"}, clear=True):
            result = choose_payment_mode()
        self.assertEqual(result, "sandbox")

    def test_dry_run_mode_when_payment_dry_run_is_1(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1"}, clear=True):
            result = choose_payment_mode()
        self.assertEqual(result, "dry-run")

    def test_raises_on_unsupported_payment_env(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "staging"}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                choose_payment_mode()
            self.assertEqual(str(ctx.exception), "unsupported payment env")


class TestChargeOrder(unittest.TestCase):
    def setUp(self):
        self.sandbox_client = Mock()
        self.gateway_client = Mock()

    def test_skipped_in_dry_run_mode(self):
        with patch.dict("os.environ", {"PAYMENT_DRY_RUN": "1"}, clear=True):
            result = charge_order(5000, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()

    def test_uses_sandbox_in_test_env(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "test"}, clear=True):
            result = charge_order(5000, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "sandbox")
        self.sandbox_client.charge.assert_called_once_with(5000)
        self.gateway_client.charge.assert_not_called()

    def test_uses_gateway_in_prod_env(self):
        with patch.dict("os.environ", {}, clear=True):
            result = charge_order(5000, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "gateway")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_called_once_with(5000)

    def test_dry_run_has_priority_over_prod(self):
        with patch.dict("os.environ", {"PAYMENT_ENV": "prod", "PAYMENT_DRY_RUN": "1"}, clear=True):
            result = charge_order(5000, self.sandbox_client, self.gateway_client)
        
        self.assertEqual(result, "skipped")
        self.sandbox_client.charge.assert_not_called()
        self.gateway_client.charge.assert_not_called()