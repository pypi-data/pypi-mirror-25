#!/usr/bin/env python
import inspect
import shutil

import os

from setuptools import setup, find_packages
from setuptools.command.install import install
from distutils.command.build import build
import tarfile
from subprocess import call
from distutils.command.clean import clean

# My reference point for this script: https://github.com/skylines-project/py-xcsoar/blob/master/setup.py
current_path = os.path.realpath(__file__).rsplit('/setup.py')[0]
cwd = os.getcwd()
print("Current Setup Location: ", current_path)
print("Working Directory: ", cwd)
__metaclass__ = type
import distutils.command.install as orig

try:
    import pypandoc
    description = pypandoc.convert('README.md', 'rst')
except:
    description = 'A library for managing redis'


def build_redis(self):
    print("Extracting Redis To Build Location: ", self.build_lib)
    tar = tarfile.open(current_path + "/redis-4.0.1.tar.gz", "r:gz")
    tar.extractall(self.build_lib)
    tar.close()

    print("Setting up  Redis make.")

    def build():
        call("make", cwd=self.build_lib + "/redis-4.0.1")

    pre = os.getcwd()
    self.execute(build, [], 'Compiling Redis')
    post = os.getcwd()
    print("Post Install Location: ", post)

    # run original build code
    # build.run(self)


class InstallRedis(install):
    def run(self):
        print("Copying Files into install...")

        build_redis(self)

        def ignore(directory, contents):
            pkgs = []
            for c in contents:
                print("Ignore: " + c)
                if c.endswith('.gz'):
                    pkgs.append(c)
                if c.endswith('tests'):
                    pkgs.append(c)
                if c.startswith('build'):
                    pkgs.append(c)
                if c.startswith('open_redis'):
                    pkgs.append(c)
            return pkgs

        install_location = self.install_lib + 'open_redis'
        try:
            print('Deleting... ' + install_location)
            shutil.rmtree(install_location + '/')
        except:
            pass
        print("Completed delete... " + install_location)

        print("Copying from ", self.build_lib, " to ", self.install_lib)
        self.copy_tree(self.build_lib, install_location)

        # TODO: this shouldn't be needed yet something is super messed up with data files
        try:
            shutil.copy(current_path + '/open_redis/redis-base-config', install_location)
            shutil.copy(current_path + '/open_redis/sentinel-base-config', install_location)
        except:
            pass

        print("Calling super run...")
        if self.old_and_unmanageable or self.single_version_externally_managed:
            return orig.install.run(self)

        if not self._called_from_setup(inspect.currentframe()):
            # Run in backward-compatibility mode to support bdist_* commands.
            orig.install.run(self)
        else:
            self.do_egg_install()


class CleanRedis(clean):
    def run(self):
        print("Cleaning time")
        if os.path.exists(self.build_temp):
            self.remove_tree(self.build_temp, dry_run=self.dry_run)


# Load Requirerments.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='open-redis',
      version='0.5',
      description='A python package to install and manage redis',
      author='John Mecham',
      author_email='jon.mecham@gmail.com',
      url='https://github.com/TheWiseLion/open-redis',
      packages=['open_redis','open_redis.pyscripts'],
      package_dir={'open_redis': 'open_redis','open_redis.pyscripts':'pyscripts'},
      keywords=['redis', 'server', 'manager'],  # arbitrary keywords
      cmdclass={
          'install': InstallRedis
      },
      entry_points={
          'console_scripts': ['redis-express=open_redis.pyscripts.redis_express:main'],
      },
      long_description=description,
      install_requires=required,
      data_files=[('open_redis/', ['open_redis/redis-base-config','open_redis/sentinel-base-config'])],
      classifiers=[
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',
          'Environment :: Console'
      ]
)
