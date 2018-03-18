import os


def write_files(files):
    for file, content in files.items():
        dir = os.path.dirname(file)
        if len(dir) > 0 and not os.path.exists(dir):
            os.makedirs(dir, mode=0O755)
        with open(file, 'w') as f:
            f.write(content)


def get_build_file(src_dir):
    # Forbid running from source dir
    if os.path.abspath(src_dir) == os.getcwd():
        raise RuntimeError("build directory should be different from source directory\n"
                           "please run this command from another directory")

    # Lookup project file
    build_file = os.path.join(src_dir, 'build.yml')
    if not os.path.isfile(build_file):
        raise IOError("%s doesn't seem to contain a build.yml file" % src_dir)

    return build_file
