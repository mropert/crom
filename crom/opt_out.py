from __future__ import print_function
import os

import configure
import tools


def opt_out(src_dir):
    try:
        project_cfg_path = tools.get_project_file(src_dir, True)
        project = tools.load_project(project_cfg_path)
        config = configure.generate(project, src_dir, exportSources=True)
        tools.write_files(config, src_dir)
        files = config.keys()
        print("Configuration files generated: " + ', '.join(files))
        os.rename('build.yml', 'build.yml.orig')
        print("Successfully opted out of crom")
        print("The old project description has been backuped as 'build.yml.orig'")
        print("To opt-in again, simply move it back to 'build.yml' and delete "
              + ' and '.join(files))

    except RuntimeError as e:
        print(e.message)
        return 1
