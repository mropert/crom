from crom.bootstrap.bootstrap import Bootstrap


def generate_lib(name):
    # Headers
    header_path = '%s/%s.hpp' % (name, name)
    file = header_path
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
    headers = {file: template.format(header_guard_define='%s_%s_HPP' % (name.upper(), name.upper()),
                                     namespace=name)}

    # Sources
    file = '%s.cpp' % name
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
    sources = {file: template.format(header_path=header_path, namespace=name)}

    # Tests
    file = '%s_test.cpp' % name
    template = (
        '// FIXME: You definitely want to include a test framework here\n'
        '#include <iostream>\n'
        '#define ASSERT(cond) \\\n'
        '   if (!(cond)) {{\\\n'
        '       std::cerr << "Assertion failed: " << #cond << std::endl;\\\n'
        '       return 1;\\\n'
        '   }}\n'
        '\n'
        '#include <{header_path}>\n'
        'using namespace {namespace};\n'
        '\n'
        'int main() {{\n'
        '   ASSERT(foo() == "Hello world!");\n'
        '   ASSERT(bar(1, 1) == 2);\n'
        '   ASSERT(bar(1, 2) == 3);\n'
        '   ASSERT(bar(0, 42) == 42);\n'
        '\n'
        '   std::cout << "All tests passed!" << std::endl;\n'
        '   return 0;\n'
        '}}\n')
    tests = {file: template.format(header_path=header_path, namespace=name)}

    return Bootstrap(name, sources, headers, tests)


def generate_exe(name):
    file = '%s.cpp' % name
    template = ('#include <iostream>\n'
                '\n'
                'int main() {\n'
                '   std::cout << "Hello world!" << std::endl;\n'
                '   return 0;\n'
                '}\n')
    return Bootstrap(name, sources={file: template})