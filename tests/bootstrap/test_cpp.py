from crom.bootstrap import cpp
from crom.project import Project


def test_generate_lib():
    project = cpp.generate_lib('hello')

    assert project.name == 'hello'
    assert project.type == Project.LIBRARY

    assert len(project.headers) == 1
    assert len(project.sources) == 1
    assert len(project.tests) == 1

    assert 'hello/hello.hpp' in project.headers
    assert 'hello.cpp' in project.sources
    assert 'hello_test.cpp' in project.tests

    assert project.headers['hello/hello.hpp'] == ('#ifndef HELLO_HELLO_HPP\n'
                                                  '#define HELLO_HELLO_HPP\n'
                                                  '\n'
                                                  '#include <string>\n'
                                                  '\n'
                                                  'namespace hello {\n'
                                                  'std::string foo();\n'
                                                  'int bar(int a, int b);\n'
                                                  '}\n'
                                                  '#endif\n')

    assert project.sources['hello.cpp'] == ('#include <hello/hello.hpp>\n'
                                            '\n'
                                            'namespace hello {\n'
                                            'std::string foo() {\n'
                                            '   return "Hello world!";\n'
                                            '}\n'
                                            '\n'
                                            'int bar(int a, int b) {\n'
                                            '   return a + b;\n'
                                            '}\n'
                                            '}\n')

    assert project.tests['hello_test.cpp'] == (
        '// FIXME: You definitely want to include a test framework here\n'
        '#include <iostream>\n'
        '#define ASSERT(cond) \\\n'
        '   if (!(cond)) {\\\n'
        '       std::cerr << "Assertion failed: " << #cond << std::endl;\\\n'
        '       return 1;\\\n'
        '   }\n'
        '\n'
        '#include <hello/hello.hpp>\n'
        'using namespace hello;\n'
        '\n'
        'int main() {\n'
        '   ASSERT(foo() == "Hello world!");\n'
        '   ASSERT(bar(1, 1) == 2);\n'
        '   ASSERT(bar(1, 2) == 3);\n'
        '   ASSERT(bar(0, 42) == 42);\n'
        '\n'
        '   std::cout << "All tests passed!" << std::endl;\n'
        '   return 0;\n'
        '}\n')


def test_generate_exe():
    project = cpp.generate_exe('hello')

    assert project.name == 'hello'
    assert project.type == Project.EXECUTABLE

    assert len(project.headers) == 0
    assert len(project.sources) == 1
    assert len(project.tests) == 0

    assert 'hello.cpp' in project.sources

    assert project.sources['hello.cpp'] == ('#include <iostream>\n'
                                            '\n'
                                            'int main() {\n'
                                            '   std::cout << "Hello world!" << std::endl;\n'
                                            '   return 0;\n'
                                            '}\n')
