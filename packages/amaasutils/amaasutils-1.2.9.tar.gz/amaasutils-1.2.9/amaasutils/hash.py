import pickle
from hashlib import sha256

def compute_hash(attributes, ignored_attributes=None):
    """
    Computes a hash code for the given dictionary that is safe for persistence round trips 
    """
    attributes = attributes.copy()

    if ignored_attributes is None:
        ignored_attributes = []

    dict_attributes = {key: value for key, value in attributes.items() if isinstance(value, dict)}
    [attributes.pop(attr) for attr in ignored_attributes + list(dict_attributes.keys())]
    
    for dict_attr_key, dict_attr_value in dict_attributes.items():
        dict_values = _flatten_dict(dict_attr_key, dict_attr_value)
        # attributes = {**attributes, **dict_values}
        attributes.update(dict_values)

    sorted_attributes = [(key, attributes[key]) for key in sorted(attributes.keys())]

    hasher = sha256()
    hasher.update(pickle.dumps(sorted_attributes))
    return hasher.hexdigest()

def _flatten_dict(dict_key, dict_value):
    results = {}
    for key, value in dict_value.items():
        if isinstance(value, dict):
            dict_values = _flatten_dict('{}.{}'.format(dict_key, key), value)
            # results = {**results, **dict_values}
            results.update(dict_values)
        else:
            results['{}.{}'.format(dict_key, key)] = value
    return results