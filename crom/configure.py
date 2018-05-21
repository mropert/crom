from __future__ import print_function
import errno
import os
from subprocess import call


from generators import cmake, conan
from project import Project
import tools


def get_build_cfg_path():
    return os.path.join(os.getcwd(), 'CMakeLists.txt')


def is_up_to_date(project_file):
    build_cfg_path = get_build_cfg_path()
    return (os.path.isfile(build_cfg_path)
            and os.path.getmtime(build_cfg_path) >= os.path.getmtime(project_file))


def mark_as_dirty():
    try:
        os.remove(get_build_cfg_path())
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def generate(project, src_dir, prefix=None, exportSources=False):
    if project.type == Project.LIBRARY:
        config = cmake.generate_lib(project, 'src', 'include', prefix)
    else:
        config = cmake.generate_exe(project, 'src', prefix)
    config.update(conan.generate(project, exportSources))
    return config


def install_dependencies(profile=None):
    args = [] if profile is None else ['-pr', profile]
    return call(['conan', 'install', '.', '--build=outdated'] + args)


def do_configure(project_cfg_path, project=None):
    # Load project file if needed
    if project is None:
        project = tools.load_project(project_cfg_path)

    print("Configuring project [%s]" % project.name)

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

    # Configure package
    ret = call(['conan', 'build', '.', '--configure'])
    if ret:
        print("configuration failed: could not configure build through conan")

    return ret


def configure(src_dir, project=None, force=False, cmd=False):
    try:
        project_cfg_path = tools.get_project_file(src_dir)

        # Check if generated build config is older than project file
        if not force and is_up_to_date(project_cfg_path):
            if cmd:
                print("configuration is up-to-date, nothing to do"
                      " (re-run with --force to generate anyway)")
            return 0

        print("Project configuration is out-of-date, reconfiguring...")
        ret = do_configure(project_cfg_path, project)
        if ret:
            mark_as_dirty()

    except RuntimeError as e:
        print(e.message)
        mark_as_dirty()
        return 1
