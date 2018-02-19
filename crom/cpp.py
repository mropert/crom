def generate_lib(name, src_dir, include_dir):
    sources = {}

    # Header file
    header_path = '%s/%s.hpp' % (name, name)
    file = '%s/%s' % (include_dir, header_path)
    template = ('#ifndef {header_guard_define}\n'
                '#define {header_guard_define}\n'
                '\n'
                '#include <string>\n'
                '\n'
                'namespace {namespace} {{\n'
                'std::string foo();\n'
                'int bar(int a, int b);\n'
                '}}\n'
                '#endif\n')
    sources[file] = template.format(header_guard_define='%s_%s_HPP' % (name.upper(), name.upper()),
                                    namespace=name)

    # Source file
    file = '%s/%s.cpp' % (src_dir, name)
    template = ('#include <{header_path}>\n'
                '\n'
                'namespace {namespace} {{\n'
                'std::string foo() {{\n'
                '   return "Hello world!";\n'
                '}}\n'
                '\n'
                'int bar(int a, int b) {{\n'
                '   return a + b;\n'
                '}}\n'
                '}}\n')
    sources[file] = template.format(header_path=header_path, namespace=name)

    return sources


def generate_exe(name):
    file = 'src/%s.cpp' % name
    template = ('#include <iostream>\n'
                '\n'
                'int main() {\n'
                '   std::cout << "Hello world!" << std::endl;\n'
                '   return 0;\n'
                '}\n')
    return {file: template}
