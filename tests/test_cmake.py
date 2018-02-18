from crom import cmake


def test_generate_simple_exe():
    files = cmake.generate('hello', ['foo.cpp'])
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_executable(hello foo.cpp)')


def test_generate_simple_exe_multiple_files():
    files = cmake.generate('hello', ['foo.cpp', 'bar.cpp', 'bazz.cpp'])
    assert len(files) == 1
    assert 'CMakeLists.txt' in files
    assert files['CMakeLists.txt'] == ('cmake_minimum_required(VERSION 3.2)\n'
                                       'project(hello)\n'
                                       '\n'
                                       'add_executable(hello foo.cpp bar.cpp bazz.cpp)')
