import numpy as np
from level import util
from questions import concept_manager

from util import formatter as fm


class DivideInts(concept_manager.ConceptManager):
    version = '1.0.3'
    key_str = 'dividing_ints_remainder'
    name = 'Dividing Whole Numbers'
    instructions = 'Find the quotient by dividing the following numbers'
    question_template = fm.wrap_as_mathjax('{{question}} =') + ' _______'
    answer_template = fm.wrap_as_mathjax('{{question}} = {{answer}}')
    tag_names = ['Digits', 'Remainder']
    tag_values = [['6/1', '5/1', '4/1', '3/1', '2/1', '6/2', '5/2', '4/2', '3/2'], ['None', 'Random']]

    def create_questions(self):
        questions = []
        for d1, d2 in [(6, 1), (5, 1), (4, 1), (3, 1), (2, 1), (6, 2), (5, 2), (4, 2), (3, 2)]:
            for include_remainder in [True, False]:
                questions.extend(self.create_questions_with_digits(d1, d2, include_remainder))
        return questions

    def create_questions_with_digits(self, digits1, digits2, include_remainder):
        tags = self.append_tag_by_name(f'{digits1}/{digits2}')
        tags = self.append_tag_by_index(1 if include_remainder else 0, tags)
        max_count = 50
        n1_values = util.random_whole_numbers(digits1, max_count)
        n2_values = util.random_whole_numbers(digits2, max_count)

        added_questions = []
        for n1, n2 in zip(n1_values, n2_values):
            if n2 == 1:
                continue
            quotient = n1 // n2
            rem = np.random.randint(1, n2) if include_remainder else 0
            n1b = quotient*n2 + rem
            answer_str = f'{quotient:,} R {rem}' if include_remainder else f'{quotient:,}'
            question = self._doc(f'{n1b:,} \\div {n2:,}', answer_str, self.key_str, tags)
            added_questions.append(question)
        util.put_multi(self._client, added_questions)
        return added_questions
