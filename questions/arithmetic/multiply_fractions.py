from level import util
from questions import concept_manager

from util import formatter as fm


class MultiplyFractions(concept_manager.ConceptManager):
    version = '1.0.1'
    key_str = 'multiply_fractions'
    name = 'Multiply and Divide Fractions'
    instructions = 'Evaluate the following fractions'
    question_template = fm.wrap_as_mathjax('{{question}} =') + ' _______'
    answer_template = fm.wrap_as_mathjax('{{question}} = {{answer}}')
    tag_names = ['Fraction Type', 'Operation']
    tag_values = [['Simple fraction', 'Improper fraction', 'Mixed number'], ['Multiplication', 'Division']]

    def _fraction_product_doc(self, n1, d1, n2, d2, is_mixed_number, is_division):
        """ Returns None for either term having a whole number for denominator or when is_mixed_number for a simple fraction."""
        n1, d1 = fm.reduce_fraction(n1, d1)
        if n1 == 1 and d1 == 1:
            return None
        n2, d2 = fm.reduce_fraction(n2, d2)
        if n2 == 1 and d2 == 1:
            return None
        op_str, op_tag_index = ('\\div', 1) if is_division else ('\\cdot', 0)
        q_str = fm.fraction_as_mathjax(n1, d1) + op_str + fm.fraction_as_mathjax(n2, d2)
        if is_division:
            n2, d2 = d2, n2
        na, da = fm.reduce_fraction(n1*n2, d1*d2)
        if is_mixed_number:
            if na < da:
                return None
            a_str = fm.separated_fraction_as_mathjax(na, da)
            return self._doc(q_str, a_str, self.key_str, [2, op_tag_index])
        else:
            a_str = fm.fraction_as_mathjax(na, da)
            if na == da:  # 1/1 is not a fraction and can only be shown as a mixed number
                return None
            if na < da:  # Simple Fraction
                return self._doc(q_str, a_str, self.key_str, [0, op_tag_index])
            else:  # Improper Fraction
                return self._doc(q_str, a_str, self.key_str, [1, op_tag_index])

    def create_questions(self):
        max_denominator = 10
        max_questions = 500

        questions = []
        for d1 in range(2, max_denominator):
            for d2 in range(d1, max_denominator):
                for n1 in range(1, d1):
                    for n2 in range(1, d2):
                        for is_mixed_number in [True, False]:
                            for is_division in [True, False]:
                                question = self._fraction_product_doc(n1, d1, n2, d2, is_mixed_number, is_division)
                                if question:
                                    questions.append(question)

        questions = self._max_sized_subset(questions, max_questions)
        util.put_multi(self._client, questions)
        return questions
