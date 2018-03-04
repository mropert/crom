from collections import OrderedDict
import yaml

from project import Project


def represent_ordereddict(dumper, data):
    value = []

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


def to_yaml(project):
    yaml.add_representer(OrderedDict, represent_ordereddict)
    return yaml.dump(OrderedDict([('name', project.name), ('sources', project.sources),
                                  ('headers', project.headers), ('tests', project.tests)]),
                     default_flow_style=False)


def from_yaml(stream):
    data = yaml.load(stream)
    return Project(data.name, data.sources, data.headers, data.tests)
