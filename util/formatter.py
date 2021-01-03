import collections
import math
import re

FormattedQuestion = collections.namedtuple('FormattedQuestion', 'question answer image_filename')

# Common symbols
math_degrees = '^\\text{o}'
implies = ' &#8658; '

# Internal constants
_rounding_error = 1E-8


def get_formatted_questions(concept, questions):
    """Returns list of FormattedQuestions using templates of the concept."""
    formatted_questions = []

    def replace_q(s):
        if 'question' in q:
            s = s.replace('{{question}}', q['question'])
        # if 'image_id' in q:
        #     s = s.replace('{{image_id}}', q['image_id'])
        return s
    concept_key = concept.key.name
    for q in questions:
        q_str = replace_q(concept['question_template'])
        a_str = replace_q(concept['answer_template']).replace('{{answer}}', q['answer'])
        image_fn = concept_key + '_' + q['image_id'] + '.png' if 'image_id' in q else None
        formatted_questions.append(FormattedQuestion(q_str, a_str, image_fn))
    return formatted_questions


def fraction_as_mathjax(n, d):
    """Mathjax format of fraction."""
    return '\\frac{' + str(n) + '}{' + str(d) + '}'


def reduced_fraction_as_mathjax(n, d):
    """Mathjax format of reduced fraction."""
    n, d = reduce_fraction(n, d)
    return fraction_as_mathjax(n, d)


def ratio_as_decimal_str(n, d, max_places=10):
    """Formatted string of ratio with truncated decimal points.
    e.g. 1, 8, 42 => "1.25"
    e.g. 1, 3, 4  => "1.3333"
    """
    ratio = n/d
    for p in range(max_places):
        if math.fabs(round(ratio, p) - ratio) < _rounding_error:
            if p == 0:
                return '%d' % int(ratio)
            return ('{0:.%df}' % p).format(ratio)
    return ('{0:.%df}' % max_places).format(ratio)


def separated_fraction_as_mathjax(n, d):
    """Mathjax formatted fraction which separates whole number."""
    if n == 0:
        return '0'
    is_negative = n < 0
    if n < 0:
        n = -n
    whole = n // d
    n = n % d
    neg_str = '-' if is_negative else ''
    pieces = []
    if whole > 0:
        pieces.append(str(whole))
    if n > 0:
        pieces.append(reduced_fraction_as_mathjax(n, d))
    return neg_str + ' '.join(pieces)


def wrap_as_mathjax(s):
    """Returns string wrapped in mathjax syntax for use in html."""
    math_start = '\\('
    math_end = '\\)'
    return math_start + s + math_end

# q_count = 0
# def inc_count():
#     global q_count
#     q_count = q_count +1
#     print(f'Adding question {q_count}')


def float_as_mathjax(value):
    """Returns string of attempted mathjax formatting of the given floating point value."""
    is_negative = False
    inf = 1E12
    if value < -_rounding_error:
        is_negative = True
        value = -value
    vals = [
        (1.0, '1'), (0.0, '0'),
        (1/4, '1/4'), (0.5, '1/2'), (3/4, '3/4'), (3/2, '3/2'),
        (1/6, '1/6'), (1/3, '1/3'), (2/3, '2/3'), (5/6, '5/6'),
        (math.sqrt(2) / 2, 'sqrt(2) / 2'), (math.sqrt(2), 'sqrt(2)'),
        (math.sqrt(3) / 2, 'sqrt(3) / 2'), (math.sqrt(3), 'sqrt(3)'),
        (math.sqrt(3), 'sqrt(3)'), (1/math.sqrt(3), '1/sqrt(3)')]
    result = None
    for val, val_str in vals:
        if math.fabs(value - val) < _rounding_error:
            result = val_str
            result = re.sub('sqrt\\((.*)\\)', '\\\\sqrt{\\1}', result)
    if math.fabs(value) > inf:
        result = 'undefined'
        is_negative = False
    if not result:
        result = f'{value:.4f}'
    if is_negative:
        result = '-' + result
    return result


def reduce_fraction(n, d):
    """Returns reduced tuple of numerator and denominator with positive denominator."""
    if d < 0:  # put any negativity into the numerator
        n, d = -n, -d
    gcf = math.gcd(n, d)
    return n // gcf, d // gcf


def factors_as_str(n, d=1, expr=None, symbol='/'):
    """Returns a simplified string for the expression: n*expr/d."""
    if n == 0:
        return '0'
    n, d = reduce_fraction(n, d)
    divisor_str = f' {symbol} {d}' if d != 1 else ''
    is_neg = False
    if n < 0:
        is_neg ^= True
        n = -n
    if expr and expr[0] == '-':
        is_neg ^= True
        expr = expr[1:]
    sign_prefix = '-' if is_neg else ''
    multipliers = []
    if n != 1:
        multipliers.append(str(n))
    if expr and expr != '1':
        multipliers.append(expr)
    if not multipliers:
        multipliers.append('1')
    multipliers_str = ' '.join(multipliers)  # no symbol is needed to imply multiplication
    return sign_prefix + multipliers_str + divisor_str


def sum_terms(terms):
    """Returns string concatenation as sum (handles negatives and zeros)."""
    result = ' + '.join([t for t in terms if t.strip() != '0'])
    # Adding a negative is just like subtracting (plus is a special char in a regex and is thus escaped)
    result = re.sub('\\+ -', '-', result)
    return result
