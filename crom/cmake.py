def concat_lines(*blocks):
    return '\n'.join(filter(None, blocks))


def concat_sections(*blocks):
    return '\n\n'.join(filter(None, blocks))


def header_decl(name):
    template = ("cmake_minimum_required(VERSION 3.2)\n"
                "project({name})")
    return template.format(name=name)


def deps_decl(name, deps):
    if len(deps) == 0:
        return None

    return '\n'.join(map(lambda p: ('target_link_libraries(%s %s %s)' % (name, p[1], p[0])), deps))


def exe_decl(name, sources, deps=[]):
    template = "add_executable({name} {sources})"
    return concat_lines(template.format(name=name, sources=' '.join(sources)),
                        deps_decl(name, deps))


def tests_decl(project, test_dir):
    if len(project.tests) == 0:
        return None

    test_name = "%s_test" % project.name
    template = "add_test(NAME {test_name} COMMAND {test_name})"
    return concat_lines('enable_testing()',
                        exe_decl(test_name, project.list_tests(test_dir),
                                 [(project.name, 'PRIVATE')]),
                        template.format(test_name=test_name))


def generate_lib(project, src_dir, include_dir, test_dir):
    template = ("add_library({name} {files})\n"
                "target_include_directories({name} PUBLIC {include_dir})\n"
                "target_include_directories({name} PRIVATE {src_dir})")
    files = ' '.join(project.list_sources_and_headers(src_dir, include_dir))
    content = concat_sections(header_decl(project.name),
                              template.format(name=project.name, files=files, src_dir=src_dir,
                                              include_dir=include_dir),
                              tests_decl(project, test_dir))
    return {'CMakeLists.txt': content + '\n'}


def generate_exe(project, src_dir):
    content = concat_sections(header_decl(project.name),
                              exe_decl(project.name, project.list_sources(src_dir)))
    return {'CMakeLists.txt': content + '\n'}
