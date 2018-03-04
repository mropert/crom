def with_directory(file, dir):
    if dir is None:
        return file
    else:
        return'/'.join([dir, file])


def list_files(files, dir):
    return sorted(map(lambda f: with_directory(f, dir), files))


def get_files(files, dir):
    return dict(map(lambda p: (with_directory(p[0], dir), p[1]), files.items()))


class Project:
    def __init__(self, name, sources={}, headers={}, tests={}):
        self.name = name
        self.sources = sources
        self.headers = headers
        self.tests = tests

    def list_sources(self, src_dir=None):
        return list_files(self.sources.keys(), src_dir)

    def list_headers(self, include_dir=None):
        return list_files(self.headers.keys(), include_dir)

    def list_tests(self, test_dir=None):
        return list_files(self.tests.keys(), test_dir)

    def list_sources_and_headers(self, src_dir=None, include_dir=None):
        return self.list_sources(src_dir) + self.list_headers(include_dir)

    def list_all_files(self, src_dir=None, include_dir=None, test_dir=None):
        return (self.list_sources(src_dir) + self.list_headers(include_dir)
                + self.list_tests(test_dir))

    def get_all_files(self, src_dir=None, include_dir=None, test_dir=None):
        files = get_files(self.sources, src_dir)
        files.update(get_files(self.headers, include_dir))
        files.update(get_files(self.tests, test_dir))
        return files
