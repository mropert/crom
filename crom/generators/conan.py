from mako.template import Template
import os


template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


def generate(project, exportSources=False):
    template_file = os.path.join(template_dir, 'conanfile.py.mako')
    # Mako's file constructor doesn't handle CRLF well...
    with open(template_file, 'r') as f:
        template = Template(f.read())
    exports = "'include/*', 'src/*', 'test/*', 'CMakeLists.txt'" if exportSources else 'None'
    return {'conanfile.py': template.render(name=project.name, sources=exports,
                                            deps=project.target.deps,
                                            test_deps=project.tests.deps)}
