def generate_exe(name):
    file = 'src/%s.cpp' % name
    template = ('#include <iostream>\n'
                '\n'
                'int main() {\n'
                '   std::cout << "Hello world!" << std::endl;\n'
                '   return 0;\n'
                '}\n')
    return {file: template}
