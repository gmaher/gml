import numpy as np

def dropFields(d, num_fields):
    keys = list(d.keys())
    num_keys = len(keys)
    if num_fields >= num_keys:
        raise RuntimeError("num_fields {} bigger than number of keys {}".format(
            num_fields, num_keys
        ))

    keys_to_drop = np.random.choice(keys, num_fields)
    for k in keys_to_drop: d[k] = None

    return d
