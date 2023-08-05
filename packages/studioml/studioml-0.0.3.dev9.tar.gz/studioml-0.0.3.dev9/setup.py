import os
import shutil
from setuptools import setup
from subprocess import call
from setuptools.command.install import install
from setuptools.command.develop import develop
import pickle


def read(fname):
    try:
        with open(os.path.join(os.path.dirname(__file__), fname)) as f:
            data = f.read()
            return data
    except BaseException:
        return None


def local_scheme(version):
    return ""
    import re
    from setuptools_scm import get_version
    full_version = get_version()
    split_version = re.split(r'dev..', full_version)
    if len(split_version) > 1:
        local_suffix = str(re.split(r'dev..', full_version)[-1])
        return '.dev' + local_suffix + '0'
    else:
        return ''


# This file contains metadata related to the studioml client and python base
# server software


class MyDevelop(develop):
    def run(self):
        # print " >>> MyDevelop with verison {} <<< ".format(VERSION)
        call(["pip install -r requirements.txt --no-clean"], shell=True)
        copyconfig()
        develop.run(self)


class MyInstall(install):

    def run(self):
        # print " >>> MyInstall with verison {} <<< ".format(VERSION)
        call(["pip install -r requirements.txt --no-clean"], shell=True)
        copyconfig()
        install.run(self)


def copyconfig():
    config_path = os.path.expanduser('~/.studioml/config.yaml')
    default_config_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "studio/default_config.yaml")

    if not os.path.exists(config_path):
        if not os.path.exists(os.path.dirname(config_path)):
            os.makedirs(os.path.dirname(config_path))

        shutil.copyfile(
            default_config_path,
            os.path.expanduser('~/.studioml/config.yaml'))


with open('requirements.txt') as f:
    required = f.read().splitlines()

with open('test_requirements.txt') as f:
    test_required = f.read().splitlines()

# projects using the studioml pthon APIs will need to use this installer
# to access the google and AWS cloud storage

setup(
    name='studioml',
    # version=VERSION,
    description='TensorFlow model and data management tool',
    packages=['studio'],
    long_description=read('README.rst'),
    url='https://github.com/studioml/studio',
    license='Apache License, Version 2.0',
    keywords='TensorFlow studioml StudioML Studio Keras scikit-learn',
    author='Illia Polosukhin',
    author_email='illia.polosukhin@gmail.com',
    data_files=[('test_requirements.txt')],
    scripts=[
            'studio/scripts/studio',
            'studio/scripts/studio-ui',
            'studio/scripts/studio-run',
            'studio/scripts/studio-runs',
            'studio/scripts/studio-local-worker',
            'studio/scripts/studio-remote-worker',
            'studio/scripts/studio-start-remote-worker',
            'studio/scripts/studio-add-credentials',
            'studio/scripts/gcloud_worker_startup.sh',
            'studio/scripts/ec2_worker_startup.sh'],
    tests_suite='nose.collector',
    tests_require=test_required,
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
    cmdclass={'develop': MyDevelop, 'install': MyInstall},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Utilities",
        "License :: OSI Approved :: Apache Software License",
    ],
    install_requires=required,
    include_package_data=True,
    zip_safe=False)
