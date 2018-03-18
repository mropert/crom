import os

from project import Project


def write_files(files, root=os.getcwd()):
    for file, content in files.items():
        dir = os.path.join(root, os.path.dirname(file))
        if len(dir) > 0 and not os.path.exists(dir):
            os.makedirs(dir, mode=0O755)
        with open(os.path.join(root, file), 'w') as f:
            f.write(content)


def get_project_file(src_dir, allow_in_source=False):
    # Forbid running from source dir
    if not allow_in_source and os.path.abspath(src_dir) == os.getcwd():
        raise RuntimeError("build directory should be different from source directory\n"
                           "please run this command from another directory")

    # Lookup project file
    build_file = os.path.join(src_dir, 'build.yml')
    if not os.path.isfile(build_file):
        raise RuntimeError("%s doesn't seem to contain a build.yml file" % src_dir)

    return build_file


def load_project(path):
    try:
        with open(path, 'r') as f:
            project = Project.from_yaml(f)
    except Exception as e:
        raise RuntimeError("could not load project configuration: " + str(e))

    return project
