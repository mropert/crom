from __future__ import print_function

import argparse
import sys

import build
import configure
import tools
from bootstrap import cpp


def generate_exe(name, src_dir):
    bootstrap = cpp.generate_exe(name)
    project = bootstrap.to_project(src_dir)

    files = bootstrap.get_all_files(src_dir=src_dir)
    files['build.yml'] = project.to_yaml()
    return files


def generate_lib(name, src_dir, include_dir, test_dir):
    bootstrap = cpp.generate_lib(name)
    project = bootstrap.to_project(src_dir, include_dir, test_dir)

    files = bootstrap.get_all_files(src_dir, include_dir, test_dir)
    files['build.yml'] = project.to_yaml()
    return files


def cmd_bootstrap(*argv):
    parser = argparse.ArgumentParser(prog="crom bootstrap")
    parser.add_argument("kind", help="the kind of project (lib or exe)", choices=['lib', 'exe'])
    parser.add_argument("name", help="the name of the project")
    args = parser.parse_args(*argv)
    name = args.name

    # Generate files
    if args.kind == 'lib':
        files = generate_lib(name, 'src', 'include', 'test')
    else:
        files = generate_exe(name, 'src')

    # Write files to disk
    tools.write_files(files)

    # Output summary
    print("The following files have been generated:")
    for file in sorted(files.keys()):
        print("- " + file)


def cmd_configure(*argv):
    parser = argparse.ArgumentParser(prog="crom configure")
    parser.add_argument("path", help="path to the project sources")
    parser.add_argument("-f", "--force", help="force re-configuration regardless of timestamps",
                        default=False, action='store_true')
    args = parser.parse_args(*argv)
    return configure.configure(args.path, args.force)


def cmd_build(*argv):
    parser = argparse.ArgumentParser(prog="crom build")
    parser.parse_args(*argv)
    return build.build()


def usage():
    print("usage: crom <command>")
    print("  bootstrap      start a new project")
    print("  build          build a project")
    print("  configure      configure a project for build")
    print('Try "crom <command> -h" to get help on a given command')


def run():
    argv = sys.argv[1:]
    commands = {'bootstrap': cmd_bootstrap, 'build': cmd_build, 'configure': cmd_configure}
    if len(argv) == 0 or argv[0] not in commands.keys():
        usage()
        return 1
    return commands[argv[0]](argv[1:])


if __name__ == "__main__":
    # execute only if run as a script
    run()
