from crom.project import Project


def test_constructor():
    sources = {'bar.cpp': 'x', 'foo.cpp': 'y'}
    headers = {'hello/bar.hpp': 'z', 'hello/foo.hpp': 'w'}
    tests = {'test.cpp': 't'}
    project = Project('hello', sources=sources, headers=headers, tests=tests)
    assert project.name == 'hello'
    assert project.sources == sources
    assert project.headers == headers
    assert project.tests == tests


def test_list_files():
    sources = {'bar.cpp': 'x', 'foo.cpp': 'y'}
    headers = {'hello/bar.hpp': 'z', 'hello/foo.hpp': 'w'}
    tests = {'test.cpp': 't'}
    project = Project('hello', sources=sources, headers=headers, tests=tests)
    assert project.list_sources('src') == ['src/bar.cpp', 'src/foo.cpp']
    assert project.list_headers('include') == ['include/hello/bar.hpp', 'include/hello/foo.hpp']
    assert project.list_tests('test') == ['test/test.cpp']
    assert project.list_sources_and_headers('src', 'include') == (
        project.list_sources('src') + project.list_headers('include'))
    assert project.list_all_files('src', 'include', 'test') == (
        project.list_sources('src') + project.list_headers('include') + project.list_tests('test'))


def test_list_files_unsorted():
    sources = {'foo.cpp': 'y', 'bar.cpp': 'x'}
    headers = {'hello/bazz.hpp': 'b', 'hello/foo.hpp': 'w', 'hello/bar.hpp': 'z'}
    tests = {'test.cpp': 't'}
    project = Project('hello', sources=sources, headers=headers, tests=tests)
    assert project.list_all_files('src', 'include', 'test') == [
        'src/bar.cpp', 'src/foo.cpp',
        'include/hello/bar.hpp', 'include/hello/bazz.hpp', 'include/hello/foo.hpp',
        'test/test.cpp'
    ]


def test_list_files_with_empty_directory():
    sources = {'bar.cpp': 'x', 'foo.cpp': 'y'}
    headers = {'hello/bar.hpp': 'z', 'hello/foo.hpp': 'w'}
    tests = {'test.cpp': 't'}
    project = Project('hello', sources=sources, headers=headers, tests=tests)
    assert project.list_all_files() == [
        'bar.cpp', 'foo.cpp',
        'hello/bar.hpp', 'hello/foo.hpp',
        'test.cpp'
    ]


def test_get_files():
    sources = {'bar.cpp': 'x', 'foo.cpp': 'y'}
    headers = {'hello/bar.hpp': 'z', 'hello/foo.hpp': 'w'}
    tests = {'test.cpp': 't'}
    project = Project('hello', sources=sources, headers=headers, tests=tests)
    assert project.get_all_files() == {
        'bar.cpp': 'x', 'foo.cpp': 'y',
        'hello/bar.hpp': 'z', 'hello/foo.hpp': 'w',
        'test.cpp': 't'
    }
