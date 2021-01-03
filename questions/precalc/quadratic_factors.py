import math

from questions.precalc import quadratic_intercepts
from util import formatter as fm


class QuadraticIntercepts(quadratic_intercepts.QuadraticIntercepts):
    version = '1.0.2'
    key_str = 'factor_quadratic'
    name = 'Factor Quadratic Equations'
    instructions = 'Factor each quadratic equation'

    def _answer(self, a, x0, x1):
        factor = math.gcd(a, x0)
        a, x0 = a // factor, x0 // factor
        prefix = str(factor) if factor > 1 else ''
        factor1_str = fm.sum_terms([fm.factors_as_str(a, 1, 'x'), str(x0)])
        factor2_str = fm.sum_terms(['x', str(x1)])
        return f'{prefix}({factor1_str})({factor2_str})'
