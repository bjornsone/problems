import os
import sympy as sp
import util.formatter as fm
from level import util, diagram_maker
from questions import concept_manager


class PythTheorem(concept_manager.ConceptManager):
    version = '1.0.12'
    key_str = 'pyth_theorem'
    name = 'Pythagorean Theorem'
    instructions = 'Solve for x in the shown triangle'
    question_template = ''
    answer_template = 'x = ' + fm.wrap_as_mathjax('{{answer}}')
    tag_names = ['Requested Side', 'Number Format']
    tag_values = [['Hypotenuse', 'Leg'], ['Whole', 'Fraction', 'Sqrt']]

    def create_questions(self):
        added_questions = []

        triangles = [(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)]
        image_id = 300
        for triangle in triangles:
            for unknown_side in range(3):
                for divisor in range(1, 12):
                    # If the divisor doesn't go in evenly to any of the sides, skip this divisor
                    if all([side % divisor != 0 for side in triangle]):
                        continue
                    is_leg = unknown_side != 2
                    tags = self.append_tag_by_index(1 if is_leg else 0)
                    tags = self.append_tag_by_index(1 if divisor > 1 else 0, tags)

                    labels = [str(sp.simplify(s)/divisor) for s in triangle]
                    added_questions.append(self._doc('', labels[unknown_side], self.key_str, tags, str(image_id)))
                    si = diagram_maker.SegmentImage()
                    si.add_right_triangle(triangle[0], triangle[2], triangle[1])
                    labels[unknown_side] = "x=?"
                    si.add_side_labels([labels[0], labels[2], labels[1]])
                    si.save(os.path.join('static', 'images', 'questions', f'{self.key_str}_{image_id}.png'))
                    image_id = image_id + 1

        util.put_multi(self._client, added_questions)
        return added_questions
