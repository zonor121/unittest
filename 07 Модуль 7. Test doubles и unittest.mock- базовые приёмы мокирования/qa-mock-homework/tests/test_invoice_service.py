import unittest
from unittest.mock import Mock

from billing.invoice_service import InvoiceService, Invoice, ChargeResult


class TestInvoiceService(unittest.TestCase):
    def setUp(self):
        self.invoice_repo = Mock()
        self.payment_gateway = Mock()
        self.service = InvoiceService(self.invoice_repo, self.payment_gateway)

    def test_successful_payment(self):
        invoice = Invoice(id=1, customer_id="cust_42", amount=5000, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        self.payment_gateway.charge.return_value = ChargeResult(
            ok=True,
            transaction_id="tx-100"
        )

        result = self.service.pay(invoice_id=1)

        self.assertEqual(result, "paid")
        self.invoice_repo.get_by_id.assert_called_once_with(1)
        self.payment_gateway.charge.assert_called_once_with("cust_42", 5000)
        self.invoice_repo.mark_paid.assert_called_once_with(1, "tx-100")
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()

    def test_declined_payment(self):
        invoice = Invoice(id=1, customer_id="cust_42", amount=5000, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        self.payment_gateway.charge.return_value = ChargeResult(
            ok=False,
            reason="insufficient_funds"
        )

        result = self.service.pay(invoice_id=1)

        self.assertEqual(result, "failed")
        self.payment_gateway.charge.assert_called_once_with("cust_42", 5000)
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_called_once_with(1, "insufficient_funds")
        self.invoice_repo.mark_retry.assert_not_called()

    def test_already_paid_invoice(self):
        invoice = Invoice(id=1, customer_id="cust_42", amount=5000, status="paid")
        self.invoice_repo.get_by_id.return_value = invoice

        result = self.service.pay(invoice_id=1)

        self.assertEqual(result, "already_paid")
        self.payment_gateway.charge.assert_not_called()
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()

    def test_invoice_not_found(self):
        self.invoice_repo.get_by_id.return_value = None

        with self.assertRaises(LookupError):
            self.service.pay(invoice_id=999)

        self.payment_gateway.charge.assert_not_called()
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()

    def test_invalid_amount(self):
        invoice = Invoice(id=1, customer_id="cust_42", amount=-100, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice

        with self.assertRaises(ValueError):
            self.service.pay(invoice_id=1)

        self.payment_gateway.charge.assert_not_called()
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_not_called()

    def test_payment_gateway_timeout(self):
        invoice = Invoice(id=1, customer_id="cust_42", amount=5000, status="pending")
        self.invoice_repo.get_by_id.return_value = invoice
        self.payment_gateway.charge.side_effect = TimeoutError("gateway timeout")

        result = self.service.pay(invoice_id=1)

        self.assertEqual(result, "retry")
        self.payment_gateway.charge.assert_called_once_with("cust_42", 5000)
        self.invoice_repo.mark_paid.assert_not_called()
        self.invoice_repo.mark_failed.assert_not_called()
        self.invoice_repo.mark_retry.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main(verbosity=2)