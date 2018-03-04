from __future__ import print_function

import argparse
import os

import build
from bootstrap import cmake
from bootstrap import cpp


def generate_exe(name, src_dir):
    bootstrap = cpp.generate_exe(name)
    project = bootstrap.to_project(src_dir)
    cmakefiles = cmake.generate_exe(project, src_dir)

    files = bootstrap.get_all_files(src_dir=src_dir)
    files.update(cmakefiles)
    files['build.yml'] = build.to_yaml(project)
    return files


def generate_lib(name, src_dir, include_dir, test_dir):
    bootstrap = cpp.generate_lib(name)
    project = bootstrap.to_project(src_dir, include_dir, test_dir)
    cmakefiles = cmake.generate_lib(project, src_dir, include_dir)

    files = bootstrap.get_all_files(src_dir, include_dir, test_dir)
    files.update(cmakefiles)
    files['build.yml'] = build.to_yaml(project)
    return files


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", help="the kind of project (lib or exe)", choices=['lib', 'exe'])
    parser.add_argument("name", help="the name of the project")
    args = parser.parse_args()
    name = args.name

    # Generate files
    if args.kind == 'lib':
        files = generate_lib(name, 'src', 'include', 'test')
    else:
        files = generate_exe(name, 'src')

    # Write files to disk
    for file, content in files.items():
        dir = os.path.dirname(file)
        if len(dir) > 0 and not os.path.exists(dir):
            os.makedirs(dir, mode=0O755)
        with open(file, 'w') as f:
            f.write(content)

    # Output summary
    print("The following files have been generated:")
    for file in sorted(files.keys()):
        print("- " + file)


if __name__ == "__main__":
    # execute only if run as a script
    run()
