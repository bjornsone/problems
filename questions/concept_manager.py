import numpy as np
from google.cloud import datastore
from level import util

class ConceptManager:

    def __init__(self):
        self._client = datastore.Client()

    def _doc(self, q_str, a_str, concept_str, tags=None, image_id=None):
        if tags==None:
            tags = []
        q_key = self._client.key('Question')
        q_doc = datastore.Entity(q_key)
        properties = {'question': q_str, 'answer': a_str, 'concept': concept_str}
        if image_id:
            properties['image_id'] = image_id
        for index, tag in enumerate(tags):
            properties[f'tag{index}'] = tag
        q_doc.update(properties)
        return q_doc

    def append_tag_by_name(self, tag_value_name, tags=None):
        """Helper method in forming list of tag_value indexes. """
        if not tags:
            tags = []
        tag_values = self.tag_values[len(tags)]
        tag_value_index = tag_values.index(tag_value_name)
        tags.append(tag_value_index)
        return tags

    def append_tag_by_index(self, tag_value_index, tags=None):
        """Helper method in forming list of tag_value indexes. """
        if not tags:
            tags = []
        try:
            for index in tag_value_index:
                tags.append(index)
        except TypeError:
            tags.append(tag_value_index)

        return tags

    def replace_tag_by_name(self, tag_value_name, tags):
        return self.append_tag_by_name(tag_value_name, tags[:-1])

    def replace_tag_by_index(self, tag_value_index, tags):
        return self.append_tag_index(tag_value_index, tags[:-1])

    def delete_questions(self, concept_str):
        client = datastore.Client()
        query = client.query(kind='Question')
        query.add_filter('concept', '=', concept_str)
        docs = [doc for doc in query.fetch()]
        # TODO(P2): Filter to query only keys
        # print(docs)
        keys = [doc.key for doc in docs]
        print(f'Deleting {len(docs)} Questions of {concept_str}')
        util.delete_multi(client, keys)

    def _max_sized_subset(self, values, max_count):
        if len(values) <= max_count:
            return values
        return np.random.choice(values, size=max_count, replace=False).tolist()
