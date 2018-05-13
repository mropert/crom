from crom.project import Project


def test_constructor():
    sources = ['bar.cpp', 'foo.cpp']
    headers = ['hello/bar.hpp', 'hello/foo.hpp']
    tests = ['test/test.cpp']
    project = Project('hello', 'lib', sources=sources, headers=headers, tests=tests)
    assert project.name == 'hello'
    assert project.type == 'lib'
    assert project.target.sources == sources
    assert project.target.headers == headers
    assert project.tests.sources == tests


def test_constructor_unsorted():
    sources = ['foo.cpp', 'bar.cpp']
    headers = ['hello/bazz.hpp', 'hello/foo.hpp', 'hello/bar.hpp']
    tests = ['test/test.cpp']
    project = Project('hello', 'lib', sources=sources, headers=headers, tests=tests)
    assert project.target.sources == ['bar.cpp', 'foo.cpp']
    assert project.target.headers == ['hello/bar.hpp', 'hello/bazz.hpp', 'hello/foo.hpp']
    assert project.tests.sources == ['test/test.cpp']
