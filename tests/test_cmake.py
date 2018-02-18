from crom import cmake


def test_generate_lib():
    files = cmake.generate_lib('hello', ['src/foo.cpp', 'include/foo/foo.hpp'], 'src', 'include')
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_library(hello src/foo.cpp include/foo/foo.hpp)\n'
                                       'target_include_directories(hello PUBLIC include)\n'
                                       'target_include_directories(hello PRIVATE src)\n')


def test_generate_lib_custom_dirs():
    files = cmake.generate_lib('hello', ['xxx/foo.cpp', 'zzz/foo/foo.hpp'], 'xxx', 'zzz')
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_library(hello xxx/foo.cpp zzz/foo/foo.hpp)\n'
                                       'target_include_directories(hello PUBLIC zzz)\n'
                                       'target_include_directories(hello PRIVATE xxx)\n')


def test_generate_lib_multiple_files():
    files = cmake.generate_lib('hello', ['src/foo.cpp',
                                         'src/bar.cpp',
                                         'include/foo/foo.hpp',
                                         'include/foo/bar.hpp'],
                               'src', 'include')
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_library(hello src/foo.cpp src/bar.cpp'
                                       ' include/foo/foo.hpp include/foo/bar.hpp)\n'
                                       'target_include_directories(hello PUBLIC include)\n'
                                       'target_include_directories(hello PRIVATE src)\n')


def test_generate_exe():
    files = cmake.generate_exe('hello', ['foo.cpp'])
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_executable(hello foo.cpp)\n')


def test_generate_exe_multiple_files():
    files = cmake.generate_exe('hello', ['foo.cpp', 'bar.cpp', 'bazz.cpp'])
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_executable(hello foo.cpp bar.cpp bazz.cpp)\n')
