from crom import cmake
from crom.project import Project


def test_generate_lib():
    project = Project('hello', sources={'foo.cpp': None}, headers={'foo/foo.hpp': None})
    files = cmake.generate_lib(project, 'src', 'include', 'test')
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_library(hello src/foo.cpp include/foo/foo.hpp)\n'
                                       'target_include_directories(hello PUBLIC include)\n'
                                       'target_include_directories(hello PRIVATE src)\n')


def test_generate_lib_with_test():
    project = Project('hello', sources={'foo.cpp': None}, headers={'foo/foo.hpp': None},
                      tests={'test.cpp': None})
    files = cmake.generate_lib(project, 'src', 'include', 'test')
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_library(hello src/foo.cpp include/foo/foo.hpp)\n'
                                       'target_include_directories(hello PUBLIC include)\n'
                                       'target_include_directories(hello PRIVATE src)\n'
                                       '\n'
                                       'enable_testing()\n'
                                       'add_executable(hello_test test/test.cpp)\n'
                                       'target_link_libraries(hello_test PRIVATE hello)\n'
                                       'add_test(NAME hello_test COMMAND hello_test)\n')


def test_generate_lib_custom_dirs():
    project = Project('hello', sources={'foo.cpp': None}, headers={'foo/foo.hpp': None})
    files = cmake.generate_lib(project, 'xxx', 'zzz', 'test')
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_library(hello xxx/foo.cpp zzz/foo/foo.hpp)\n'
                                       'target_include_directories(hello PUBLIC zzz)\n'
                                       'target_include_directories(hello PRIVATE xxx)\n')


def test_generate_lib_multiple_files():
    project = Project('hello', sources={'foo.cpp': None, 'bar.cpp': None},
                      headers={'foo/foo.hpp': None, 'foo/bar.hpp': None})

    files = cmake.generate_lib(project, 'src', 'include', 'test')
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_library(hello src/bar.cpp src/foo.cpp'
                                       ' include/foo/bar.hpp include/foo/foo.hpp)\n'
                                       'target_include_directories(hello PUBLIC include)\n'
                                       'target_include_directories(hello PRIVATE src)\n')


def test_generate_exe():
    project = Project('hello', sources={'foo.cpp': None})
    files = cmake.generate_exe(project, None)
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_executable(hello foo.cpp)\n')


def test_generate_exe_multiple_files():
    project = Project('hello', sources={'foo.cpp': None, 'bar.cpp': None, 'bazz.cpp': None})
    files = cmake.generate_exe(project, None)
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_executable(hello bar.cpp bazz.cpp foo.cpp)\n')
