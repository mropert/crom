def generate_header(name):
    template = ("cmake_minimum_required(VERSION 3.2)\n"
                "project({name})\n")
    return template.format(name=name)


def generate_lib(name, sources, src_dir, include_dir):
    template = ("add_library({name} {sources})\n"
                "target_include_directories({name} PUBLIC {include_dir})\n"
                "target_include_directories({name} PRIVATE {src_dir})\n")
    content = (generate_header(name)
               + "\n"
               + template.format(name=name, sources=' '.join(sources),
                                 src_dir=src_dir, include_dir=include_dir))
    return {'CMakeLists.txt': content}


def generate_exe(name, sources):
    template = "add_executable({name} {sources})\n"
    content = generate_header(name) + "\n" + template.format(name=name, sources=' '.join(sources))
    return {'CMakeLists.txt': content}
