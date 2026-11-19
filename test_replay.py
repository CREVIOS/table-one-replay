import unittest
from fractions import Fraction
from io import StringIO

from replay import EXAMPLE, bin_predictions, calibration_errors


class ReplayTests(unittest.TestCase):
    def test_six_predictions(self):
        with EXAMPLE.open(encoding="utf-8", newline="") as source:
            bins = bin_predictions(source)
        self.assertEqual(len(bins), 15)
        self.assertEqual(bins[8], (2, 2, Fraction(6, 5)))
        self.assertEqual(bins[13], (4, 3, Fraction(18, 5)))
        self.assertEqual(calibration_errors(bins), (Fraction(7, 30), Fraction(1, 30)))

    def test_bin_edges(self):
        bins = bin_predictions(StringIO("confidence,correct\n0,0\n1/15,0\n1,1\n"))
        self.assertEqual(bins[0], (2, 0, Fraction(1, 15)))
        self.assertEqual(bins[-1], (1, 1, 1))

    def test_invalid_inputs(self):
        for row in ("", "1.2,1", "0.6,2", "nan,1", "0.6,1,extra"):
            with self.subTest(row=row), self.assertRaises(ValueError):
                bin_predictions(StringIO("confidence,correct\n" + row))


if __name__ == "__main__":
    unittest.main()
