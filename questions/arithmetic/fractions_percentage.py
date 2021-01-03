from level import util
from questions import concept_manager

from util import formatter as fm


class ConvertFractionsPercents(concept_manager.ConceptManager):
    version = '1.0.1'
    key_str = 'convert_fracs_pct'
    name = 'Converting Fractions and Percentage'
    instructions = 'Convert between fractions and percentages'
    question_template = fm.wrap_as_mathjax('{{question}} =') + ' _______'
    answer_template = fm.wrap_as_mathjax('{{question}} = {{answer}}')
    tag_names = ['Direction', 'Size', 'Denominator']
    tag_values = [['To Percent', 'To Fraction'], ['Below One', 'Above One'], ['10 or Below', '11 to 19', '20 or Above']]

    def create_questions(self):
        denoms = [2, 4, 5, 8, 10, 16, 20, 25]

        added_questions = []
        finished = set()
        for d in denoms:
            for n in range(1, d*3//2):
                if d == n:
                    continue
                n2, d2 = fm.reduce_fraction(n, d)
                if n2/d2 in finished:
                    continue
                finished.add(n2/d2)
                tag1 = 0 if n2 < d2 else 1
                tag2 = 0 if d2 <= 10 else (1 if d2 <= 19 else 2)
                frac_str = fm.fraction_as_mathjax(n2, d2)
                pct_str = fm.ratio_as_decimal_str(100*n, d) + '\\%'
                question = self._doc(frac_str, pct_str, self.key_str, [0, tag1, tag2])
                added_questions.append(question)
                question = self._doc(pct_str, frac_str, self.key_str, [1, tag1, tag2])
                added_questions.append(question)
        util.put_multi(self._client, added_questions)
        return added_questions
