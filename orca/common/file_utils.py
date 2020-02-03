import yaml


def load_yaml(path):
    data = None
    with open(path, 'r') as stream:
        data = yaml.load(stream, Loader=yaml.BaseLoader)
    return data
