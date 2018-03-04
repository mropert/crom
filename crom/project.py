class Project:
    def __init__(self, name, sources=[], headers=[], tests=[]):
        self.name = name
        self.sources = sorted(sources)
        self.headers = sorted(headers)
        self.tests = sorted(tests)
