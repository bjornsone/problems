from google.cloud import datastore

from questions.arithmetic import multiply_ints, divide_ints
from questions.arithmetic import add_fractions_com_den, fractions_percentage, multiply_fractions
from questions.precalc import trigonometry, quadratic_intercepts, quadratic_vertex, quadratic_factors
from questions.precalc import sum_diff_factoring, linear_equations, pyth_theorem


def put_level(parent_obj, level_type, level_value, name, client, contents=None, force_rewrite=False):
    parent_key = parent_obj.key if parent_obj else None
    key = client.key(level_type, level_value, parent=parent_key)
    if not force_rewrite:
        # Try to load an existing version
        level_obj = datastore.Entity(key)
        if level_obj:
            return

    level_obj = datastore.Entity(key)
    full_name = (parent_obj['full_name'] + ',' + name) if parent_obj else name
    if not contents:
        contents = {}
    contents['name'] = name
    contents['full_name'] = full_name
    level_obj.update(contents)
    client.put(level_obj)
    return level_obj


def latest_concept_version_exists(parent_obj, concept_manager, client):
    """Returns whether the version in the code matches the version in the DB."""
    key = client.key('Concept', concept_manager.key_str, parent=parent_obj.key)
    concept_obj = client.get(key)
    if not concept_obj:
        return False
    return 'version' in concept_obj and concept_obj['version'] == concept_manager.version


def put_concept(topic_obj, concept_manager, client, force_rewrite=False):
    """Writes the concept and all contained questions if it is not current."""
    if not force_rewrite:
        if latest_concept_version_exists(topic_obj, concept_manager, client):
            return

    concept_manager.delete_questions(concept_manager.key_str)
    questions = concept_manager.create_questions()
    print(f'Creating {len(questions)} questions for {concept_manager.name}')
    question_keys = [question.key for question in questions]
    contents = {'instructions': concept_manager.instructions,
                'question_template': concept_manager.question_template,
                'answer_template': concept_manager.answer_template,
                'version': concept_manager.version,
                'tag_names': concept_manager.tag_names,
                'question_keys': question_keys}
    for i, tag_values in enumerate(concept_manager.tag_values):
        contents[f'tag{i}_values'] = tag_values
    concept_obj = put_level(
        topic_obj, 'Concept', concept_manager.key_str, concept_manager.name, client, contents, force_rewrite=True)
    return concept_obj


def create_hierarchy(force_rewrite=False):
    """Creates all levels, concepts and questions."""
    client = datastore.Client()
    subject_math = put_level(None, 'Subject', 'math', 'Mathematics', client, force_rewrite=force_rewrite)

    # COURSE: Precalculus
    course_precalc = put_level(subject_math, 'Course', 'precalc', 'Precalculus', client, force_rewrite=force_rewrite)

    # Triangles
    topic_triangles = put_level(course_precalc, 'Topic', 'triangles', 'Triangles', client, force_rewrite=force_rewrite)
    put_concept(topic_triangles, pyth_theorem.PythTheorem(), client, force_rewrite=force_rewrite)

    # Trigonometry
    topic_trigonometry = put_level(course_precalc, 'Topic', 'trigonometry', 'Trig Functions', client, force_rewrite=force_rewrite)
    put_concept(topic_trigonometry, trigonometry.Trigonometry(), client, force_rewrite=force_rewrite)

    # Linear
    topic_linear = put_level(course_precalc, 'Topic', 'linear_eqn', 'Linear Equations', client, force_rewrite=force_rewrite)
    put_concept(topic_linear, linear_equations.LinearEquations(), client, force_rewrite=force_rewrite)

    # Quadratic
    topic_quadratic = put_level(course_precalc, 'Topic', 'quadratic_eqn', 'Quadratic Equations', client, force_rewrite=force_rewrite)
    put_concept(topic_quadratic, quadratic_intercepts.QuadraticIntercepts(), client, force_rewrite=force_rewrite)
    put_concept(topic_quadratic, quadratic_vertex.QuadraticVertex(), client, force_rewrite=force_rewrite)
    put_concept(topic_quadratic, quadratic_factors.QuadraticIntercepts(), client, force_rewrite=force_rewrite)

    # Cubic
    topic_cubic = put_level(course_precalc, 'Topic', 'cubic_eqn', 'Cubic Equations', client, force_rewrite=force_rewrite)
    put_concept(topic_cubic, sum_diff_factoring.SumAndDiffFactoring(), client, force_rewrite=force_rewrite)

    #  COURSE: Arithmetic
    course_arithmetic = put_level(subject_math, 'Course', 'arithmetic', 'Arithmetic', client, force_rewrite=force_rewrite)
    # Integer Multiplication
    topic_multiplication = put_level(course_arithmetic, 'Topic', 'multiplication', 'Multiplication', client, force_rewrite=force_rewrite)
    put_concept(topic_multiplication, multiply_ints.MultiplyInts(), client, force_rewrite=force_rewrite)
    # Integer Division
    topic_division = put_level(course_arithmetic, 'Topic', 'division', 'Division', client, force_rewrite=force_rewrite)
    put_concept(topic_division, divide_ints.DivideInts(), client, force_rewrite=force_rewrite)

    # Fractions
    topic_fractions = put_level(course_arithmetic, 'Topic', 'fractions', 'Fractions', client, force_rewrite=force_rewrite)
    put_concept(topic_fractions, add_fractions_com_den.AddFractionsComDen(), client, force_rewrite=force_rewrite)
    put_concept(topic_fractions, fractions_percentage.ConvertFractionsPercents(), client, force_rewrite=force_rewrite)
    put_concept(topic_fractions, multiply_fractions.MultiplyFractions(), client, force_rewrite=force_rewrite)
