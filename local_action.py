from google.cloud import datastore

from level import creator
from level import util


def delete_all(level_kind):
    client = datastore.Client()
    # with client.transaction():  # Including the transaction limited the max deletion size
    query = client.query(kind=level_kind)
    # TODO(P2): Filter to query only keys
    docs = [doc.key for doc in query.fetch()]
    print(f'Deleting {len(docs)} {level_kind}s')
    util.delete_multi(client, docs)


def delete_all_levels():
    for level_kind in ['Course', 'Topic', 'Concept']:  # , 'Question']:
        delete_all(level_kind)


if __name__ == '__main__':
    # delete_all_levels()
    creator.create_hierarchy(False)
