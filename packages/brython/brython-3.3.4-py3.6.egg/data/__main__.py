import os
import shutil
import json
import argparse

import list_modules

def main(args=None):
    """The main routine."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--install', help='Install Brython in an empty directory',
        action="store_true")
    parser.add_argument('--make_dist',
        help='Make a Python distribution',
        action="store_true")
    parser.add_argument('--modules',
        help='Create brython_modules.js with all the modules used by the application',
        action="store_true")
    parser.add_argument('--reset', help='Reset brython_modules.js to stdlib',
        action="store_true")
    parser.add_argument('--update', help='Update Brython scripts',
        action="store_true")
    args = parser.parse_args()

    files = 'README.txt', 'demo.html', 'brython.js', 'brython_stdlib.js'

    src_path = os.path.dirname(__file__)
    dest = os.path.join(os.getcwd(), 'brython')

    if args.install:
        print('Installing Brython in subdirectory brython')

        if not os.path.exists(dest):
            os.mkdir(dest)

        for path in files:
            shutil.copyfile(os.path.join(src_path, path),
                os.path.join(dest, path))

    if args.update:
        print('Update Brython scripts')

        if not os.path.exists(dest):
            os.mkdir(dest)

        for path in files:
            shutil.copyfile(os.path.join(src_path, path),
                os.path.join(dest, path))

    if args.reset:
        print('Reset brython_modules.js to standard distribution')
        shutil.copyfile(os.path.join(os.getcwd(), 'brython_stdlib.js'),
            os.path.join(os.getcwd(), 'brython_modules.js'))

    if args.modules:
        print('Create brython_modules.js with all the modules used by the application')
        finder = list_modules.ModulesFinder()
        finder.inspect()
        finder.make_brython_modules()

    if args.make_dist:
        print('Make a Python distribution for the application')
        finder = list_modules.ModulesFinder()
        finder.inspect()
        finder.make_brython_modules()
        finder.make_setup()
        print('done')

if __name__ == "__main__":
    main()