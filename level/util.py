import numpy as np
import time


def put_multi(client, docs, chunk_size=100):
    for chunk in [docs[i:i + chunk_size] for i in range(0, len(docs), chunk_size)]:
        client.put_multi(chunk)


def delete_multi(client, keys, chunk_size=100):
    """Deletes all provided keys."""
    for chunk in [keys[i:i + chunk_size] for i in range(0, len(keys), chunk_size)]:
        client.delete_multi(chunk)


def timeit(method):
    """Can be a decorator @timeit before a function."""
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result
    return timed


def random_whole_numbers(digits, result_size):
    min, max = 10 ** (digits - 1), 10 ** digits
    return random_subset(range(min, max), result_size)


def random_subset(values, result_size):
    with_replacement = False
    if len(values) < result_size:
        with_replacement = True
    return np.random.choice(values, size=result_size, replace=with_replacement).tolist()

