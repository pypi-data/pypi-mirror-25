import os
import sys

from setuptools import setup, find_packages

import list_modules

if os.path.exists('README.rst'):
    with open('README.rst', encoding='utf-8') as fobj:
        LONG_DESCRIPTION = fobj.read()

# Values to customize
app_name = None
version = None
url = ""
author = ""
author_email = ""
license = "BSD"

if app_name is None:
    print("No name for the application. Please edit setup.py"
        " and set app_name")
    sys.exit()

if version is None:
    print("No version number for the application."
        " Please edit setup.py and set version")
    sys.exit()

finder = list_modules.ModulesFinder()
finder.inspect()
finder.prepare_dist(app_name)

# Get files
files = []
dir_length = len(os.path.join(os.getcwd(), "__dist__")) + 1
for dirname, dirnames, filenames in os.walk("__dist__"):
    for filename in filenames:
        path = os.path.join(dirname, filename)[9:]
        print(path)
        files.append(path)

setup(
    name=app_name,
    version=version,

    # The project's main homepage.
    url=url,

    # Author details
    author=author,
    author_email=author_email, 
    
    # License
    license=license,
       
    packages=['__dist__'],
    py_modules=[app_name],
    package_data={'__dist__':files}
)