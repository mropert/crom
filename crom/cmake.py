def generate(name, sources):
    template = ("cmake_minimum_required(VERSION 3.2)\n"
                "project({name})\n"
                "\n"
                "add_executable({name} {sources})"
                )
    return {'CMakeLists.txt': template.format(name=name, sources=' '.join(sources))}
