
def list_of_dicts_to_dict(list_of_dicts):
    return dict([ (key, d[key]) for d in list_of_dicts for key in d ])
