from level import util
from questions import concept_manager

from util import formatter as fm


class QuadraticVertex(concept_manager.ConceptManager):
    version = '1.0.4'
    key_str = 'find_quad_vertex'
    name = 'Finding Vertex of Parabola'
    instructions = 'Find y-intercepts of a given quadratic equation'
    question_template = fm.wrap_as_mathjax('y = {{question}}')
    answer_template = (fm.wrap_as_mathjax('y = {{question}} ') + fm.implies +
                       '(' + fm.wrap_as_mathjax('{{answer}}' + ')'))
    tag_names = ['First Coefficient', 'Direction']
    tag_values = [['1', '2', '3'], ['Up', 'Down']]

    def _create_quad_vertex_doc(self, coeff, dx, dy):
        # y = coeff*(x-dx)^2 + dy
        x1 = -2*dx*coeff
        x0 = dx*dx*coeff + dy
        q_str = fm.sum_terms(
            [fm.factors_as_str(coeff, 1, 'x^2'),
             fm.factors_as_str(x1, 1, 'x'),
             fm.factors_as_str(x0, 1)])
        a_str = '%s, %s' % (fm.factors_as_str(dx, 1), fm.factors_as_str(dy, 1))
        tags = self.append_tag_by_name(str(abs(coeff)))
        tags = self.append_tag_by_index(0 if coeff > 0 else 1, tags)
        return self._doc(q_str, a_str, self.key_str, tags)

    def create_questions(self):
        added_questions = []

        dxs = range(-6, 7)
        dys = range(-4, 4)
        coeffs = [-2, -1, 1, 2, 3]
        for dx in dxs:
            for dy in dys:
                for coeff in coeffs:
                    question = self._create_quad_vertex_doc(coeff, dx, dy)
                    added_questions.append(question)
        util.put_multi(self._client, added_questions)
        return added_questions
