from conans import ConanFile, CMake


class ConanProject(ConanFile):
    name = "${name}"
    version = "0.1"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ${sources}

%if len(deps) > 0 or len(test_deps) > 0:
    def requirements(self):
    %for d in deps:
        self.requires('${d}')
    %endfor
    %if len(test_deps) > 0:
        if self.develop:
        %for d in test_deps:
            self.requires('${d}')
        %endfor
    %endif

%endif
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
