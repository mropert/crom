from crom.bootstrap.bootstrap import Bootstrap


def test_bootstrap():
    bootstrap = Bootstrap('hello', {'hello.cpp': None}, {'hello/hello.hpp': None},
                                   {'hello_test.cpp': None})
    project = bootstrap.to_project()
    assert project.name == 'hello'
    assert len(project.headers) == 1
    assert len(project.sources) == 1
    assert len(project.tests) == 1

    assert 'hello/hello.hpp' in project.headers
    assert 'hello.cpp' in project.sources
    assert 'hello_test.cpp' in project.tests


def test_get_files():
    sources = {'bar.cpp': 'x', 'foo.cpp': 'y'}
    headers = {'hello/bar.hpp': 'z', 'hello/foo.hpp': 'w'}
    tests = {'test.cpp': 't'}
    bootstrap = Bootstrap('hello', sources=sources, headers=headers, tests=tests)
    assert bootstrap.get_all_files() == {
        'bar.cpp': 'x', 'foo.cpp': 'y',
        'hello/bar.hpp': 'z', 'hello/foo.hpp': 'w',
        'test.cpp': 't'
    }
