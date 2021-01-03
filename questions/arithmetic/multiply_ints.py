from level import util
from questions import concept_manager

from util import formatter as fm


class MultiplyInts(concept_manager.ConceptManager):
    version = '1.0.0'
    key_str = 'multiply_ints'
    name = 'Multiplying Whole Numbers'
    instructions = 'Find the product by multiplying the following numbers'
    question_template = fm.wrap_as_mathjax('{{question}} =') + ' _______'
    answer_template = fm.wrap_as_mathjax('{{question}} = {{answer}}')
    tag_names = ['digits']
    tag_values = [['1x1', '2x1', '3x1', '2x2', '3x2', '3x3']]

    def create_questions(self):
        max_digits = 3
        questions = []
        for d1 in range(1, max_digits + 1):
            for d2 in range(1, d1 + 1):
                questions.extend(self.create_questions_with_digits(d1, d2))
        return questions

    def create_questions_with_digits(self, digits1, digits2):
        tags = self.append_tag_by_name(f'{digits1}x{digits2}')
        max_count = 10
        d1_values = util.random_whole_numbers(digits1, max_count)
        d2_values = util.random_whole_numbers(digits2, max_count)

        added_questions = []
        for d1 in d1_values:
            for d2 in d2_values:
                # Always put the biggest value first
                if d2 > d1:
                    d1, d2 = d2, d1
                question = self._doc(f'{d1} \\times {d2}', str(d1 * d2), self.key_str, tags)
                added_questions.append(question)
        util.put_multi(self._client, added_questions)
        return added_questions
