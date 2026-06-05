import unittest

from shop.pricing import final_price_cents


class TestPricingScenarios(unittest.TestCase):
    def test_standard_retail_scenario(self):
        base = 5000
        discount = 15
        tax = 20
        result = final_price_cents(base, discount, tax)
        expected = 5100
        self.assertEqual(result, expected)

    def test_bulk_order_with_high_discount(self):
        base = 50000
        discount = 30
        tax = 20
        result = final_price_cents(base, discount, tax)
        expected = 42000
        self.assertEqual(result, expected)

    def test_multiple_products_chain(self):
        products = [
            (1000, 0, 20),
            (2000, 10, 20),
            (500, 5, 10),
        ]
        total = sum(final_price_cents(*p) for p in products)
        expected_total = 3882
        self.assertEqual(total, expected_total)