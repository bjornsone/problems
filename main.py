import util.formatter as fm
import numpy as np
import hashlib

from flask import Flask, render_template
from flask import request, redirect
from google.cloud import datastore

from level import finder
from util import request_util as ru

app = Flask(__name__)


def add_filter_tags(query, tag_dict):
    """ Adds filtering to query based on dictionary of tags. """
    is_filter_complete = True
    for tag_name, tag_values in tag_dict.items():
        # Datastore can only pre-filter for a single matching item.
        # When the user selects multiple acceptable values, we can't filter on it in the query.
        # Such cases need to be filtered after retrieving all of the objects.
        if len(tag_values) == 1:
            for tag_value in tag_values:
                query.add_filter(tag_name, '=', tag_value)
        else:
            is_filter_complete = False
    return is_filter_complete


def filter_questions(questions, tag_dict):
    """Returns list of questions which is a subset of the provided questions filtered by tag_dict."""
    good_questions = []
    for q in questions:
        is_bad = False
        for tag_name, tag_values in tag_dict.items():
            q_tag_value = q[tag_name]
            if q_tag_value not in tag_values:
                is_bad = True
        if not is_bad:
            good_questions.append(q)
    return good_questions


def get_request_int(name, default):
    p_str = request.args.get(name, None)
    if not p_str:
        return default
    try:
        return int(p_str)
    except (ValueError, TypeError):
        return default


def process_seeds(show_answers):
    if show_answers:
        a_seed = get_request_int('a_seed', np.random.randint(0, 0xffffff))
        a_seed_bytes = a_seed.to_bytes(4, 'big')
        q_seed_hashed_bytes = hashlib.md5(a_seed_bytes).digest()
        q_seed = int.from_bytes(q_seed_hashed_bytes[:4], byteorder='big')
    else:
        a_seed = None
        q_seed = get_request_int('q_seed', np.random.randint(0, 0xffffff))

    # Set the seed
    print(f'SEEDING: {q_seed}')
    np.random.seed(q_seed)
    return q_seed, a_seed


def get_questions(concept_obj, max_count=30):
    client = datastore.Client()

    # Get keys of all questions that meet the tag and concept name requirements
    query = client.query(kind='Question')
    query.keys_only()
    print(concept_obj.key.name)
    query.add_filter('concept', '=', concept_obj.key.name)
    query_tag_dict = ru.get_tag_dict_from_params(concept_obj)
    is_filter_complete = add_filter_tags(query, query_tag_dict)
    tag_question_keys = [doc.key for doc in query.fetch()]

    # Restrict to only keys within this concept (if concepts are versioned, this will remove old questions
    # that are no longer part of this version of the concept (even if they meet the tag requirements).
    keys = set(tag_question_keys).intersection(set(concept_obj['question_keys']))

    if is_filter_complete:
        # Restrict count
        result_len = max_count if len(keys) > max_count else len(keys)
        keys = np.random.choice(list(keys), result_len, False).tolist()

        questions = client.get_multi(keys=keys)
    else:
        questions = client.get_multi(keys=list(keys))
        questions = filter_questions(questions, query_tag_dict)
        result_len = max_count if len(questions) > max_count else len(questions)

    if len(questions) == 0:
        return questions

    questions = np.random.choice(questions, result_len, False).tolist()
    return questions


def get_full_paths(level_obj):
    """ Returns list of paths for each level of parentage except the last.

    Such paths are useful in constructing URLs that link to each parent level (e.g. a link to the course).
    """
    full_path = ''
    full_paths = []
    for path in level_obj.key.flat_path[1::2]:
        full_path = full_path + '/' + path
        full_paths.append(full_path)
    full_paths[-1] = None  # There shouldn't be a link to the deepest level (which is itself)
    return full_paths


@app.route('/outline/<subject>/<course>/<topic>')
@app.route('/outline/<subject>/<course>', defaults={'topic': None})
@app.route('/outline/<subject>', defaults={'course': None, 'topic': None})
@app.route('/outline', defaults={'subject': 'math', 'course': None, 'topic': None})
@app.route('/', defaults={'subject': 'math', 'course': None, 'topic': None})
def root(subject, course, topic):
    client = datastore.Client()
    print('DEBUG: ', subject, course, topic)
    level_obj = finder.get_level(client, subject, course, topic)
    level_depth = len(level_obj['full_name'].split(','))
    print('\nXXX DEBUG: ', level_obj)
    concept_tuples = finder.get_child_concepts(client, subject, course, topic)
    return render_template('outline.html',
                           level_obj=level_obj, level_depth=level_depth, full_paths=get_full_paths(level_obj),
                           concept_tuples=concept_tuples)


@app.route('/concept_sheet/<subject>/<course>/<topic>/<concept>')
def concept_sheet(subject, course, topic, concept):
    # TODO: Make these (and other display properties) part of the concept
    dx, dy = 4, 7
    client = datastore.Client()

    show_ans = get_request_int('show_ans', 1)
    q_seed, a_seed = process_seeds(show_answers=show_ans)

    concept_obj = finder.get_level(client, subject, course, topic, concept)
    questions = get_questions(concept_obj, max_count=dx * dy)  # TODO: Handle error when filtering gives zero questions.
    formatted_questions = fm.get_formatted_questions(concept_obj, questions)
    formatted_questions_2d = [formatted_questions[y * dx:y * dx + dx] for y in range(dy)]

    redirect_path = f'/concept_sheet/{subject}/{course}/{topic}/{concept}'

    show_ans_params = f'show_ans={show_ans}'
    seed_params = f'a_seed={a_seed}' if show_ans else f'q_seed={q_seed}'
    new_seed_params = f'a_seed={np.random.randint(0, 0xffffff)}'
    no_answer_seed_params = f'q_seed={q_seed}'

    tag_dict = ru.get_tag_dict_from_params(concept_obj)
    tag_param_str = ru.get_url_param_str_from_tag_dict(tag_dict)

    params = {}
    params['nontag'] = ru.catenate_params(show_ans_params, seed_params)
    params['shuffle'] = ru.catenate_params(show_ans_params, new_seed_params, tag_param_str)
    params['no_answer'] = ru.catenate_params('show_ans=0', no_answer_seed_params, tag_param_str)

    return render_template('concept_sheet.html', concept_obj=concept_obj,
                           level_obj=concept_obj, full_paths=get_full_paths(concept_obj),
                           redirect_path=redirect_path, params=params, show_answers=show_ans,
                           tag_dict=tag_dict, questions_list=formatted_questions_2d)


@app.route('/concept_list/<subject>/<course>/<topic>/<concept>')
def concept_list(subject, course, topic, concept):
    dy = 10
    client = datastore.Client()

    # TODO: Update HTML to match params
    concept_obj = finder.get_level(client, subject, course, topic, concept)
    questions = get_questions(concept_obj, max_count=dy)
    formatted_questions = fm.get_formatted_questions(concept_obj, questions)

    redirect_path = f'/concept_sheet/{subject}/{course}/{topic}/{concept}'

    tag_dict = ru.get_tag_dict_from_params(concept_obj)

    return render_template('concept_list.html', concept_obj=concept_obj,
                           level_obj=concept_obj, full_paths=get_full_paths(concept_obj),
                           redirect_path=redirect_path, tag_dict=tag_dict, questions=formatted_questions)


@app.route('/tag_filter', methods=['POST'])
def tag_filter():
    """Processes posted form into filtering parameters of an URL and redirects to that URL."""
    tag_param_str = ru.get_url_param_str_from_tag_dict(ru.get_tag_dict_from_form())
    nontag_param_str = request.form.get("nontag_params")
    param_str = ru.catenate_params(tag_param_str, nontag_param_str)
    url = request.form.get("redirect_path") + '?' + param_str
    return redirect(url, code=302)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
