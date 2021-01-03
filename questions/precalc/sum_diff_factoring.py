import math
import numpy as np
import sympy as sp

from level import util
from questions import concept_manager
from util import formatter as fm

# sum_squares/sum_cubes/diff_cubes var_const/var_var x/other_names power:3,6,9
# 8x^3 - 27y^6 = (2x-3y^2)(4x^2+6xy^4)


class SumAndDiffFactoring(concept_manager.ConceptManager):
    version = '1.0.3'
    key_str = 'sum_and_diff_factoring'
    name = 'Finding Factors of Basic Polynomials'
    instructions = 'Factor the polynomial'
    question_template = fm.wrap_as_mathjax('y = {{question}}')
    answer_template = fm.wrap_as_mathjax('y = {{question}} ') + fm.implies + '<br/>' + fm.wrap_as_mathjax('{{answer}}')
    tag_names = ['Type', 'Second Term', 'Power']
    tag_values = [['Diff of Squares', 'Sum of Cubes', 'Diff of Cubes'],
                  ['Constant', 'Other Variable'],
                  ['Simple', 'Higher Order']]

    def _answer(self, a, x0, x1):
        return '%s, %d' % (fm.factors_as_str(-x0, a), -x1)

    def create_questions(self):
        added_questions = []

        constants = range(1, 5)
        var_names = ['x', 'y', 'a', 'b', 'c']
        extra_powers = [(1, 1), (2, 1), (3, 1), (2, 3)]  # , (3, 2), (5, 3)]

        for c1 in constants:
            for c2 in constants:
                if math.gcd(c1, c2) != 1:  # Don't include the same factor in both
                    continue
                for v1 in var_names:
                    for has_second_var in [False, True]:
                        v2 = var_names[np.random.randint(0, len(var_names))] if has_second_var else None
                        if v2 == v1:
                            continue
                        for ep1, ep2 in extra_powers:
                            # Difference of Squares
                            # c1^2*v1^(ep[0]*2) - c2^2*v2^(ep[1]*2) = (c1*v2^ep[0]-c2*v2^ep[1])*(...+...)
                            v1_sp = sp.symbols(v1)
                            term1 = c1 * v1_sp**ep1
                            term2 = c2
                            if v2:
                                v2_sp = sp.symbols(v2)
                                term2 *= v2_sp**(ep1*2)
                            tag_index1 = 1 if v2 else 0
                            tag_index2 = 0 if ep1 == 1 and ep2 == 1 else 1

                            # Difference of Squares
                            question_str = sp.latex(term1*term1 - term2*term2)
                            answer_str = sp.latex((term1+term2)*(term1-term2))
                            tags = self.append_tag_by_index(0)  # Diff of Sqares
                            tags = self.append_tag_by_index([tag_index1, tag_index2], tags)
                            added_questions.append(self._doc(question_str, answer_str, self.key_str, tags))

                            # Sum of Cubes
                            question_str = sp.latex(term1*term1*term1 + term2*term2*term2)
                            answer_str = sp.latex((term1+term2)*(term1*term1 - term1*term2 + term2*term2))
                            tags = self.append_tag_by_index(1)  # Sum of Cubes
                            tags = self.append_tag_by_index([tag_index1, tag_index2], tags)
                            added_questions.append(self._doc(question_str, answer_str, self.key_str, tags))

                            # Difference of Cubes
                            question_str = sp.latex(term1*term1*term1 - term2*term2*term2)
                            answer_str = sp.latex((term1-term2)*(term1*term1 + term1*term2 + term2*term2))
                            tags = self.append_tag_by_index(2)  # Diff of Cubes
                            tags = self.append_tag_by_index([tag_index1, tag_index2], tags)
                            added_questions.append(self._doc(question_str, answer_str, self.key_str, tags))
        util.put_multi(self._client, added_questions)
        return added_questions
