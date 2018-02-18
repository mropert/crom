from crom import cpp


def test_generate_simple_exe():
    sources = cpp.generate_exe('hello')
    assert len(sources) == 1
    assert 'src/hello.cpp' in sources
    assert sources['src/hello.cpp'] == ('#include <iostream>\n'
                                        '\n'
                                        'int main() {\n'
                                        '   std::cout << "Hello world!" << std::endl;\n'
                                        '   return 0;\n'
                                        '}\n')
