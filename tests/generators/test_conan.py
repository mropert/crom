from crom.generators import conan
from crom.project import Project


def test_generate():
    project = Project('hello', 'lib', sources={'src/foo.cpp': None},
                      headers={'include/foo/foo.hpp': None})
    files = conan.generate(project)
    assert len(files) == 1
    assert 'conanfile.py' in files
    assert files['conanfile.py'] == """from conans import ConanFile, CMake


class ConanProject(ConanFile):
    name = "hello"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if self.develop:
            cmake.test()

    def package(self):
        self.copy("*.h", dst="include", src="include")
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False, symlinks=True)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
"""
