from crom.project import Project


def with_directory(file, dir):
    if dir is None:
        return file
    else:
        return'/'.join([dir, file])


def list_files(files, dir):
    return map(lambda f: with_directory(f, dir), files)


def get_files(files, dir):
    return dict(map(lambda p: (with_directory(p[0], dir), p[1]), files.items()))


class Bootstrap:
    def __init__(self, name, type, sources={}, headers={}, tests={}, test_deps=[]):
        self.name = name
        self.type = type
        self.sources = sources
        self.headers = headers
        self.tests = tests
        self.test_deps = test_deps

    def to_project(self, src_dir=None, include_dir=None, test_dir=None):
        return Project(self.name, self.type, list_files(self.sources.keys(), src_dir),
                       list_files(self.headers.keys(), include_dir),
                       list_files(self.tests.keys(), test_dir),
                       test_deps=self.test_deps)

    def get_all_files(self, src_dir=None, include_dir=None, test_dir=None):
        files = get_files(self.sources, src_dir)
        files.update(get_files(self.headers, include_dir))
        files.update(get_files(self.tests, test_dir))
        return files
