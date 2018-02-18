from __future__ import print_function

import argparse
import os

import cmake
import cpp


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="the name of the project")
    args = parser.parse_args()
    name = args.name

    # Generate C++ sources
    sources = cpp.generate_exe(name)

    # Generate build files
    cmakefiles = cmake.generate(name, sources.keys())

    # Bundle all files to generate
    files = sources
    files.update(cmakefiles)

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
