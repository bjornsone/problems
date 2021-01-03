from flask import request


def get_tag_dict_from_params(concept_obj):
    """ Returns dict of tags based on params such as tag0=v1,v2&tag1=v3,v4"""
    tags = {}
    for tag_index in range(5):
        tag_name = f'tag{tag_index}'
        tag_values = request.args.get(tag_name, None)
        if tag_values:
            tags[tag_name] = [int(s) for s in tag_values.split(',')]
            # If all options are selected, then the filter can be removed
            if len(tags[tag_name]) == len(concept_obj[f'tag{tag_index}_values']):
                del tags[tag_name]
    # print("TAGS: ", tags)
    return tags


def catenate_params(s1=None, s2=None, s3=None, s4=None):
    ss = [s for s in [s1, s2, s3, s4] if s]
    return '&'.join(ss)


def get_tag_dict_from_form():
    """Creates dictionary of tags from submitted form.

    e.g. Checking the second option of the first tag would be a form field of tag0_1.
    """
    tag_dict = {}
    for param, value in request.form.items():
        if value != 'on':
            continue
        if not param.startswith('tag'):
            continue
        split_parts = param.split('_')
        tag_dict.setdefault(split_parts[0], []).append(int(split_parts[1]))
    # print('DEBUG TAGS', tag_dict)
    return tag_dict


def get_url_param_str_from_tag_dict(tag_dict):
    """Given a dictionary of param_str:[param_val], it converts to a URL parameter string."""
    params = [tag + '=' + ",".join([str(tag_value) for tag_value in tag_values]) for tag, tag_values in
              tag_dict.items()]
    return '&'.join(params)
