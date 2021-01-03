import random

import util.formatter as fm
import sympy as sp
from level import util
from questions import concept_manager


class LinearEquations(concept_manager.ConceptManager):
    version = '1.0.5'
    key_str = 'linear_equation'
    name = 'Linear Equation'
    instructions = 'Solve for the variable in the linear equation'
    question_template = fm.wrap_as_mathjax('{{question}}')
    answer_template = fm.wrap_as_mathjax('{{question}} ') + fm.implies + '<br/>' + fm.wrap_as_mathjax('{{answer}}')
    tag_names = ['Variable Location', 'Result']
    tag_values = [['One side', 'Both sides'], ['Integer', 'Fraction']]

    def create_questions(self):
        added_questions = []

        left_coeffs = range(-6, 6)
        net_left_coeffs = range(-6, 6)
        right_consts = range(-6, 6)
        net_right_consts = range(-6, 6)
        var_names = ['x', 'y', 'a', 'b', 'c']

        fraction_kept = 0.05
        random.seed(42)
        for left_coeff in left_coeffs:
            for net_left_coeff in net_left_coeffs:
                for right_const in right_consts:
                    for net_right_const in net_right_consts:
                        if random.uniform(0, 1) > fraction_kept:
                            continue
                        if net_left_coeff == 0:  # don't allow division by zero
                            continue
                        var_name = var_names[random.randint(0, len(var_names)-1)]
                        var = sp.symbols(var_name)
                        right_coeff = left_coeff - net_left_coeff  # net_left = left - right
                        left_const = right_const - net_right_const  # net_right = right - left
                        eqn = sp.Eq(left_coeff*var + left_const, right_coeff*var + right_const)
                        q_str = sp.latex(eqn)
                        soln = sp.solve(eqn)[0]
                        a_str = sp.latex(sp.Eq(var, soln))
                        tags = self.append_tag_by_index(0 if right_coeff == 0 else 1)
                        tags = self.append_tag_by_index(0 if soln.is_integer else 1, tags)
                        added_questions.append(self._doc(q_str, a_str, self.key_str, tags))

        util.put_multi(self._client, added_questions)
        return added_questions
