from crom import cpp


def test_generate_lib():
    sources = cpp.generate_lib('hello', 'src', 'include')
    assert len(sources) == 2
    assert 'include/hello/hello.hpp' in sources
    assert 'src/hello.cpp' in sources

    assert sources['include/hello/hello.hpp'] == ('#ifndef HELLO_HELLO_HPP\n'
                                                  '#define HELLO_HELLO_HPP\n'
                                                  '\n'
                                                  '#include <string>\n'
                                                  '\n'
                                                  'namespace hello {\n'
                                                  'std::string foo();\n'
                                                  'int bar(int a, int b);\n'
                                                  '}\n'
                                                  '#endif\n')

    assert sources['src/hello.cpp'] == ('#include <hello/hello.hpp>\n'
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


def test_generate_exe():
    sources = cpp.generate_exe('hello')
    assert len(sources) == 1
    assert 'src/hello.cpp' in sources
    assert sources['src/hello.cpp'] == ('#include <iostream>\n'
                                        '\n'
                                        'int main() {\n'
                                        '   std::cout << "Hello world!" << std::endl;\n'
                                        '   return 0;\n'
                                        '}\n')
