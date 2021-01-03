import unittest
from util import formatter as fm


class FormatterTest(unittest.TestCase):
    def test_basic_fraction_mathjax(self):
        result = fm.fraction_as_mathjax(4, 5)
        self.assertEqual(result, '\\frac{4}{5}')

    def test_reduced_fraction(self):
        result = fm.reduced_fraction_as_mathjax(8, 10)
        self.assertEqual(result, '\\frac{4}{5}')

    def test_separated_fraction(self):
        result = fm.separated_fraction_as_mathjax(13, 5)
        self.assertEqual(result, '2 \\frac{3}{5}')

    def test_ratio_as_decimal_str(self):
        result = fm.ratio_as_decimal_str(3, 4)
        self.assertEqual(result, '0.75')
        result = fm.ratio_as_decimal_str(1, 8)
        self.assertEqual(result, '0.125')
        result = fm.ratio_as_decimal_str(10, 2)
        self.assertEqual(result, '5')
        result = fm.ratio_as_decimal_str(4, 3, 3)
        self.assertEqual(result, '1.333')

    def test_basic_fraction(self):
        result = fm.factors_as_str(4, 5)
        self.assertEqual(result, '4 / 5')

    def test_neg_denom(self):
        result = fm.factors_as_str(4, -5)
        self.assertEqual(result, '-4 / 5')

    def test_unit_denominator(self):
        result = fm.factors_as_str(4, 1)
        self.assertEqual(result, '4')

    def test_unit_numerator(self):
        result = fm.factors_as_str(1, 4)
        self.assertEqual(result, '1 / 4')

    def test_unit_numerator_of_expr(self):
        result = fm.factors_as_str(1, 4, 'sin(x)')
        self.assertEqual(result, 'sin(x) / 4')

    def test_unit(self):
        result = fm.factors_as_str(1, 1)
        self.assertEqual(result, '1')

    def test_2neg(self):
        result = fm.factors_as_str(4, -5, '-foo')
        self.assertEqual(result, '4 * foo / 5')


if __name__ == '__main__':
    unittest.main()
