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


class Target:
    def __init__(self, sources=[], headers=[], deps=[]):
        self.sources = sorted(sources)
        self.headers = sorted(headers)
        self.deps = sorted(deps)

    def as_dict(self):
        return OrderedDict([('sources', self.sources), ('headers', self.headers),
                            ('dependencies', self.deps)])

    @staticmethod
    def from_dict(data):
        return Target(data.get('sources', []), data.get('headers', []), data.get('deps', []))


class Project:
    EXECUTABLE = 'exe'
    LIBRARY = 'lib'

    def __init__(self, name, type, sources=[], headers=[], tests=[], test_deps=[]):
        self.name = name
        self.type = type
        self.target = Target(sources, headers)
        self.tests = Target(tests, deps=test_deps)

    def to_yaml(self):
        d = OrderedDict([('name', self.name), ('type', self.type)])
        d.update(self.target.as_dict())
        d['tests'] = self.tests.as_dict()

        return yaml.dump(d, default_flow_style=False)

    @staticmethod
    def from_yaml(stream):
        data = yaml.load(stream)
        target = Target.from_dict(data)
        tests = Target.from_dict(data['tests'])
        return Project(data['name'], data['type'], target.sources, target.headers, tests.sources,
                       tests.deps)
