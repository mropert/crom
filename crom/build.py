from subprocess import call

import configure
import tools


def build(src_dir):
    try:
        project_cfg_path = tools.get_project_file(src_dir)

        # Re-run configuration if needed
        if not configure.is_up_to_date(project_cfg_path):
            print('configuration is out of date, reconfiguring...')
            ret = configure.do_configure(project_cfg_path)
            if ret:
                print('reconfiguration failed')
                return 1

        ret = call(['conan', 'build', '.'])
        if ret:
            print('build failed')
            return 1

        print('build successful')
        return 0

    except RuntimeError as e:
        print(e.message)
        return 1
