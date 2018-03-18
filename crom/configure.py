from __future__ import print_function
import os
from subprocess import call


from generators import cmake, conan
import tools


def is_up_to_date(project_file):
    build_cfg_path = os.path.join(os.getcwd(), 'CMakeLists.txt')
    return (os.path.isfile(build_cfg_path)
            and os.path.getmtime(build_cfg_path) >= os.path.getmtime(project_file))


def generate(project, src_dir, prefix=None, exportSources=False):
    if project.type == 'lib':
        config = cmake.generate_lib(project, 'src', 'include', prefix)
    else:
        config = cmake.generate_exe(project, 'src', prefix)
    config.update(conan.generate(project, exportSources))
    return config


def install_dependencies(profile=None):
    args = [] if profile is None else ['-pr', profile]
    return call(['conan', 'install', '.', '--build=outdated'] + args)


def do_configure(project_cfg_path):
    # Load project file
    project = tools.load_project(project_cfg_path)

    # Write configuration
    src_dir = os.path.dirname(project_cfg_path)
    config = generate(project, src_dir, os.path.relpath(src_dir))
    tools.write_files(config)
    print("Configuration files generated: " + ', '.join(config.keys()))

    # Install deps
    ret = install_dependencies()
    if ret:
        print("configuration failed: could not install dependencies")
        return 1

    return 0


def configure(src_dir, force=False):
    try:
        project_cfg_path = tools.get_project_file(src_dir)

        # Check if generated build config is older than project file
        if not force and is_up_to_date(project_cfg_path):
            print("configuration is up-to-date, nothing to do"
                  " (re-run with --force to generate anyway)")
            return 0

        return do_configure(project_cfg_path)

    except RuntimeError as e:
        print(e.message)
        return 1
