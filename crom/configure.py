from __future__ import print_function
import os

from generators import cmake, conan
from project import Project
import tools


def is_up_to_date(project_file):
    build_cfg_path = os.path.join(os.getcwd(), 'CMakeLists.txt')
    return (os.path.isfile(build_cfg_path)
            and os.path.getmtime(build_cfg_path) >= os.path.getmtime(project_file))


def generate(project, src_dir):
    if project.type == 'lib':
        config = cmake.generate_lib(project, 'src', 'include', os.path.relpath(src_dir))
    else:
        config = cmake.generate_exe(project, 'src', os.path.relpath(src_dir))
    config.update(conan.generate(project))
    tools.write_files(config)
    return config.keys()


def configure(src_dir, force=False):
    try:
        project_cfg_path = tools.get_build_file(src_dir)
    except RuntimeError as e:
        print(e.message)
        return 1

    # Check if generated build config is older than project file
    if not force and is_up_to_date(project_cfg_path):
        print("configuration is up-to-date, nothing to do (re-run with --force to generate anyway)")
        return 0

    # Load project file
    try:
        with open(project_cfg_path, 'r') as f:
            project = Project.from_yaml(f)
    except Exception as e:
        print("could not load project configuration: " + str(e))
        return 1

    # Write configuration
    files = generate(project, src_dir)
    print("Configuration files generated: " + ', '.join(files))
