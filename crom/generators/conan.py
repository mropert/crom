import os


template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')


def generate(project):
    template_file = os.path.join(template_dir, 'conanfile.py.in')
    with open(template_file, 'r') as f:
        template = f.read()
    return {'conanfile.py': template.replace('%NAME%', project.name)}
