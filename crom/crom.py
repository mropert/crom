from __future__ import print_function

import argparse
import os

import cmake
import cpp


def generate_exe(name):
    sources = cpp.generate_exe(name)
    cmakefiles = cmake.generate_exe(name, sources.keys())

    files = sources
    files.update(cmakefiles)
    return files


def generate_lib(name, src_dir, include_dir):
    sources = cpp.generate_lib(name, src_dir, include_dir)
    cmakefiles = cmake.generate_lib(name, sources.keys(), src_dir, include_dir)

    files = sources
    files.update(cmakefiles)
    return files


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", help="the kind of project (lib or exe)", choices=['lib', 'exe'])
    parser.add_argument("name", help="the name of the project")
    args = parser.parse_args()
    name = args.name

    # Generate files
    if args.kind == 'lib':
        files = generate_lib(name, 'src', 'include')
    else:
        files = generate_exe(name)

    # Write files to disk
    for file, content in files.items():
        dir = os.path.dirname(file)
        if len(dir) > 0 and not os.path.exists(dir):
            os.makedirs(dir, mode=0O755)
        with open(file, 'w') as f:
            f.write(content)

    # Output summary
    print("The following files have been generated:")
    for file in files.keys():
        print("- " + file)


if __name__ == "__main__":
    # execute only if run as a script
    run()
