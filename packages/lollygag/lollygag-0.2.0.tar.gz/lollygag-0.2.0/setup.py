#!/usr/bin/env python

from setuptools import setup, find_packages
import os
import sys
import json

here = os.path.dirname(os.path.realpath(__file__))

version_info_path = os.path.join(here, "lollygag", ".version")
try:
    with open(version_info_path, 'r') as f:
        version_info = json.loads(f.read())
except IOError:
    print("\n.version file was not found!\n")
    raise
except:
    print("Unexpected error occured while getting .version information!")
    a,b,c = sys.exc_info()
    print(a)
    print(b)
    print(c)
    sys.exit(1)

def main():
  setup(name='lollygag',
        author='Daniel Kiss',
        version=version_info["version"],
        author_email='littlesnorrboy@gmail.com',
        url='https://github.com/snorrwe/lollygag',
        description="A simple web crawling module",
        long_description=version_info["home_page"],
        license="MIT",
        package_dir={'lollygag':'lollygag'},
        packages=find_packages('.'),
        package_data={'lollygag': ['.version']},
        install_requires=['requests>=2.2.1'],
        tests_require=['tl.testing==0.5', 'pylint==1.7.2']
  )

if __name__ == '__main__':
  main()
