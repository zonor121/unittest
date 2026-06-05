import unittest

from shop.pricing import final_price_cents


class TestFinalPrice(unittest.TestCase):
    def test_base_price_no_discount_no_tax(self):
        result = final_price_cents(1000, discount_percent=0, tax_percent=0)
        self.assertEqual(result, 1000)

    def test_discount_reduces_price(self):
        result = final_price_cents(1000, discount_percent=10, tax_percent=0)
        self.assertEqual(result, 900)

    def test_tax_increases_price(self):
        result = final_price_cents(1000, discount_percent=0, tax_percent=20)
        self.assertEqual(result, 1200)

    def test_discount_and_tax_combined(self):
        result = final_price_cents(1000, discount_percent=10, tax_percent=20)
        self.assertEqual(result, 1080)

    def test_discount_100_percent_makes_free(self):
        result = final_price_cents(1000, discount_percent=100, tax_percent=20)
        self.assertEqual(result, 0)

    def test_tax_100_percent_doubles(self):
        result = final_price_cents(1000, discount_percent=0, tax_percent=100)
        self.assertEqual(result, 2000)

    def test_invalid_type_base_cents(self):
        with self.assertRaises(TypeError):
            final_price_cents("1000")

    def test_invalid_type_discount(self):
        with self.assertRaises(TypeError):
            final_price_cents(1000, discount_percent="10")

    def test_invalid_type_tax(self):
        with self.assertRaises(TypeError):
            final_price_cents(1000, tax_percent="20")

    def test_negative_base_raises(self):
        with self.assertRaises(ValueError):
            final_price_cents(-1)

    def test_discount_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, discount_percent=101)

    def test_tax_out_of_range_raises(self):
        with self.assertRaises(ValueError):
            final_price_cents(1000, tax_percent=-1)

    def test_bool_not_accepted_as_int(self):
        with self.assertRaises(TypeError):
            final_price_cents(True)