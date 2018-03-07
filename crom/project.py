from collections import OrderedDict
import yaml


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


yaml.add_representer(OrderedDict, represent_ordereddict)


class Project:
    def __init__(self, name, type, sources=[], headers=[], tests=[]):
        self.name = name
        self.type = type
        self.sources = sorted(sources)
        self.headers = sorted(headers)
        self.tests = sorted(tests)

    def to_yaml(self):
        return yaml.dump(OrderedDict([('name', self.name), ('type', self.type),
                                     ('sources', self.sources), ('headers', self.headers),
                                     ('tests', self.tests)]),
                         default_flow_style=False)

    @staticmethod
    def from_yaml(stream):
        data = yaml.load(stream)
        return Project(data['name'], data['type'], data['sources'], data['headers'], data['tests'])
