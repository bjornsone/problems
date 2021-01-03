

def _create_key(client, subject, course=None, topic=None, concept=None):
    """Creates a key based on text strings of the path."""
    if concept:
        return client.key('Subject', subject, 'Course', course, 'Topic', topic, 'Concept', concept)
    elif topic:
        return client.key('Subject', subject, 'Course', course, 'Topic', topic)
    elif course:
        return client.key('Subject', subject, 'Course', course)
    elif subject:
        return client.key('Subject', subject)
    else:
        return None


def get_level(client, subject_str, course_str=None, topic_str=None, concept_str=None):
    """Loads any level (e.g. concept) based on strings that define full path."""
    return client.get(_create_key(client, subject_str, course_str, topic_str, concept_str))


def get_child_concepts(client, subject, course=None, topic=None):
    """ For the given parent path, returns a list of Tuple[concept, path] objects.

    Each element of the list represents one concept with: (concept_name, concept_path)."""
    concepts = []
    ancestor_key = _create_key(client, subject, course, topic)
    print('Querying', ancestor_key)
    query = client.query(kind='Concept', ancestor=ancestor_key)
    # query.order = ["$key"]

    # TODO: Separate query from logic for determining paths to display
    previous_parent_path = [subject, course, topic]
    for doc in query.fetch():
        # print(doc)
        key_path = doc.key.flat_path
        key_path = key_path[1::2]
        parent_path = key_path[:-1]
        key_path_str = '/'.join(key_path)
        full_name_list = doc['full_name'].split(',')
        print(full_name_list)
        if parent_path[0] != previous_parent_path[0]:
            display_path = full_name_list[:-1]  # Nothing matches so display the whole path
        elif parent_path[1] != previous_parent_path[1]:
            display_path = full_name_list[1:-1]
        elif parent_path[2] != previous_parent_path[2]:
            display_path = full_name_list[2:-1]
        else:
            display_path = []

        concepts.append((doc, key_path_str, display_path))
        previous_parent_path = parent_path
    return concepts


