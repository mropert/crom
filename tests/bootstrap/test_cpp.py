from crom.bootstrap import cpp
from crom.project import Project


def test_generate_lib():
    project = cpp.generate_lib('hello')

    assert project.name == 'hello'
    assert project.type == Project.LIBRARY

    assert len(project.headers) == 1
    assert len(project.sources) == 1
    assert len(project.tests) == 2

    assert 'hello/hello.hpp' in project.headers
    assert 'hello.cpp' in project.sources
    assert 'hello_test.cpp' in project.tests
    assert 'main.cpp' in project.tests

    assert project.test_deps == ['catch2/2.2.2@bincrafters/stable']

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
        '#include <catch.hpp>\n'
        '\n'
        '#include <hello/hello.hpp>\n'
        'using namespace hello;\n'
        '\n'
        'TEST_CASE("foo returns hello world", "[foo]") {\n'
        '   REQUIRE(foo() == "Hello world!");\n'
        '}\n'
        '\n'
        'TEST_CASE("bar sums the arguments", "[bar]") {\n'
        '   REQUIRE(bar(1, 1) == 2);\n'
        '   REQUIRE(bar(1, 2) == 3);\n'
        '   REQUIRE(bar(0, 42) == 42);\n'
        '}\n')

    assert project.tests['main.cpp'] == (
        '#define CATCH_CONFIG_MAIN // Tell catch to build main here\n'
        '#include <catch.hpp>\n')


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
