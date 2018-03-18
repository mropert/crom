from subprocess import call


def build(profile=None):
    args = [] if profile is None else ['-pr', profile]
    ret = call(['conan', 'install', '.'] + args)
    if ret:
        print('build failed')
        return 1

    ret = call(['conan', 'build', '.'] + args)
    if ret:
        print('build failed')
        return 1

    print('build successful')
    return 0
