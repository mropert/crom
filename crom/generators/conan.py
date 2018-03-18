import os


template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


def generate(project, exportSources=False):
    template_file = os.path.join(template_dir, 'conanfile.py.in')
    with open(template_file, 'r') as f:
        template = f.read()
    exports = "'include/*', 'src/*', 'test/*', 'CMakeLists.txt'" if exportSources else 'None'
    return {'conanfile.py': template.replace('%NAME%', project.name)
                                    .replace('%EXPORTS%', exports)}
