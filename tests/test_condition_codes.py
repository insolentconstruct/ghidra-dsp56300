#!/usr/bin/env python3
"""NN/NR truth table: DSP56300 Family Manual Rev. 5, Table 12-17.

Run with python3 tests/test_condition_codes.py; checks every generated CC table.
"""
from pathlib import Path
import itertools
import re
import unittest


class ConditionCodes(unittest.TestCase):
    def test_nn_nr(self):
        spec = (Path(__file__).resolve().parents[1] /
                'data/languages/dsp56300.sinc').read_text()
        equations = re.findall(
            r'(CC\w+): "(nn|nr)" is .*?local c:1 = (.*?); export c;', spec)
        self.assertEqual({table for table, _, _ in equations}, {'CC0', 'CC12', 'CC8'})
        self.assertEqual(len(equations), 6)
        # Rows are Z,U,E in binary order. NR holds for zero or a normalized
        # mantissa with no extension; NN is its complement.
        normalized = (True, False, False, False, True, True, True, True)
        for table, name, equation in equations:
            expression = equation.replace('||', ' or ').replace('&&', ' and ')
            expression = re.sub(r'!(?!=)', ' not ', expression).strip()
            for flags, nr in zip(itertools.product((0, 1), repeat=3), normalized):
                with self.subTest(table=table, condition=name, flags=flags):
                    actual = eval(expression, {'__builtins__': {}}, dict(zip('ZUE', flags)))
                    self.assertEqual(bool(actual), nr if name == 'nr' else not nr)


if __name__ == '__main__':
    unittest.main()
