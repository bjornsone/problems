import math

from level import util
from questions import concept_manager

from util import formatter as fm


class Trigonometry(concept_manager.ConceptManager):
    version = '1.0.1'
    key_str = 'function_eval'
    name = 'Evaluating Trig Functions'
    instructions = 'Evaluate the following trigonometric expressions'
    question_template = fm.wrap_as_mathjax('{{question}} ') + ' = ________'
    answer_template = fm.wrap_as_mathjax('{{question}} = {{answer}}')
    tag_names = ['angles', 'function', 'measure']
    tag_values = [['basic', 'full 360'], ['sin', 'cos', 'tan', 'sec', 'csc'], ['degrees', 'radians']]

    def create_questions(self):
        added_questions = []
        angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 270]
        functions = {'sin': math.sin, 'cos': math.cos, 'tan': math.tan}
        for angle in angles:
            for function_name, f in functions.items():
                answer = f(angle * math.pi / 180)
                tags = self.append_tag_by_index(0 if 0 <= angle <= 90 else 1)
                tags = self.append_tag_by_name(function_name, tags)
                a = fm.float_as_mathjax(answer)
                angle_degrees = f'{str(angle)}{fm.math_degrees}'
                n, d = fm.reduce_fraction(angle, 180)
                angle_radians = fm.factors_as_str(n, d, '\\pi')
                q_degrees = f'{function_name}({angle_degrees})'
                q_radians = f'{function_name}({angle_radians})'

                tags = self.append_tag_by_name('degrees', tags)
                added_questions.append(self._doc(q_degrees, a, self.key_str, tags))

                tags = self.replace_tag_by_name('radians', tags)
                added_questions.append(self._doc(q_radians, a, self.key_str, tags))
        util.put_multi(self._client, added_questions)
        return added_questions
