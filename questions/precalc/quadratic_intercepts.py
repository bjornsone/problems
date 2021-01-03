import math

from level import util
from questions import concept_manager

from util import formatter as fm


class QuadraticIntercepts(concept_manager.ConceptManager):
    version = '1.0.7'
    key_str = 'find_factors'
    name = 'Finding Intercepts'
    instructions = 'Find x-intercepts of the given quadratic equation'
    question_template = fm.wrap_as_mathjax('y = {{question}}')
    # answer_template = fm.wrap_as_mathjax('y = {{question}} ') + fm.implies + fm.wrap_as_mathjax('{{answer}}')
    answer_template = fm.wrap_as_mathjax('y = {{question}} ') + fm.implies + '<br/>' + fm.wrap_as_mathjax('{{answer}}')
    tag_names = ['First Coefficient', 'Constant Factor']
    tag_values = [['1', '2', 'Other'], ['1', 'Other']]

    def _answer(self, a, x0, x1):
        return '%s, %d' % (fm.factors_as_str(-x0, a), -x1)

    def _quad_doc(self, a, x0, x1):
        """Create doc for factors of (ax+x0)(x+x1)"""
        q_str = fm.sum_terms(
            [fm.factors_as_str(a, 1, 'x^2'),
             fm.factors_as_str(a * x1 + x0, 1, 'x'),
             fm.factors_as_str(x0 * x1, 1)])
        a_str = self._answer(a, x0, x1)
        tags = self.append_tag_by_name(str(a) if a <= 2 else 'Other')
        tags = self.append_tag_by_index(0 if math.gcd(a, x0) == 1 else 1, tags)
        return self._doc(q_str, a_str, self.key_str, tags)

    def create_questions(self):
        added_questions = []

        intercepts = range(-6, 7)
        for x0 in intercepts:
            for x1 in intercepts:
                question = self._quad_doc(1, x0, x1)
                added_questions.append(question)
        intercepts = range(-3, 4)
        for x0 in intercepts:
            for x1 in intercepts:
                question = self._quad_doc(2, x0, x1)
                added_questions.append(question)
                question = self._quad_doc(3, x0, x1)
                added_questions.append(question)
                question = self._quad_doc(4, x0, x1)
                added_questions.append(question)
        util.put_multi(self._client, added_questions)
        return added_questions
