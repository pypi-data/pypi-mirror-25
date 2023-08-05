import yaml

def get_list_data(data):
    if isinstance(data, basestring):
        ac = []
        for doc in yaml.safe_load_all(data):
            if isinstance(doc, list):
                ac += doc
            else:
                ac.append(doc)
        data = ac
    return data
