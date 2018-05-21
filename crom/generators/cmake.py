def concat_lines(*blocks):
    return '\n'.join(filter(None, blocks))


def concat_sections(*blocks):
    return '\n\n'.join(filter(None, blocks))


def apply_prefix_function(prefix):
    return lambda f: '/'.join(filter(None, [prefix, f]))


def apply_prefix(f, prefix):
    return apply_prefix_function(prefix)(f)


def apply_prefix_l(files, prefix):
    return map(apply_prefix_function(prefix), files)


def header_decl(name):
    template = ("cmake_minimum_required(VERSION 3.2)\n"
                "project({name})\n"
                "\n"
                "include(${{CMAKE_BINARY_DIR}}/conanbuildinfo.cmake)\n"
                "conan_basic_setup()")
    return template.format(name=name)


def deps_decl(name, deps):
    if len(deps) == 0:
        return None

    return '\n'.join(map(lambda p: ('target_link_libraries(%s %s %s)' % (name, p[1], p[0])), deps))


def exe_decl(name, sources, deps=[], prefix=None):
    template = "add_executable({name} {sources})"
    return concat_lines(template.format(name=name,
                                        sources=' '.join(apply_prefix_l(sources, prefix))),
                        deps_decl(name, deps))


def tests_decl(project, prefix=None):
    if len(project.tests.sources) == 0:
        return None

    test_name = "%s_test" % project.name
    template = "add_test(NAME {test_name} COMMAND {test_name})"
    return concat_lines('enable_testing()',
                        exe_decl(test_name, project.tests.sources, [(project.name, 'PRIVATE')],
                                 prefix),
                        template.format(test_name=test_name))


def generate_lib(project, src_dir, include_dir, prefix=None):
    template = ("add_library({name} {files})\n"
                "target_include_directories({name} PUBLIC {include_dir})\n"
                "target_include_directories({name} PRIVATE {src_dir})")
    files = ' '.join(apply_prefix_l(project.target.sources + project.target.headers, prefix))
    content = concat_sections(header_decl(project.name),
                              template.format(name=project.name, files=files,
                                              src_dir=apply_prefix(src_dir, prefix),
                                              include_dir=apply_prefix(include_dir, prefix)),
                              tests_decl(project, prefix))
    return {'CMakeLists.txt': content + '\n'}


def generate_exe(project, src_dir, prefix=None):
    content = concat_sections(header_decl(project.name),
                              exe_decl(project.name, project.target.sources, prefix=prefix))
    return {'CMakeLists.txt': content + '\n'}
