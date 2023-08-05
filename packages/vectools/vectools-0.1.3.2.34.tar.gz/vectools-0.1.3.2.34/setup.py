from __future__ import print_function
import sys
import os.path
from setuptools import setup, find_packages
import io

__version__ = '0.1.3.2.34'
if __name__ == "__main__":
    # d = dirname(dirname(abspath(__file__))) # /home/kristina/desire-directory
    #real_path = "/".join(os.path.realpath(__file__).split("/")[:-1])
    #with open(real_path+"/VERSION") as f:
    #    __version__ = f.read().strip()

    # from http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
    def read(*file_names, **kwargs):
        encoding = kwargs.get('encoding', 'utf-8')
        sep = kwargs.get('sep', '\n')
        buf = []
        for filename in file_names:
            with io.open(filename, encoding=encoding) as f:
                buf.append(f.read())
        return sep.join(buf)

    long_description = read('README.txt')  # 'CHANGES.txt'

    setup(
        name="vectools",
        # MAJOR version when they make incompatible API changes,
        # MINOR version when they add functionality in a backwards-compatible manner, and
        # MAINTENANCE version when they make backwards-compatible bug fixes.
        # http://semver.org/
        version=__version__,
        packages=find_packages(),
        license='MIT',
        author='Tyler Weirick',
        author_email='tyler.weirick@gmail.com',
        install_requires=[
            # Used with the program.
            'numpy>=1.9.2',
            'scipy>=0.16.0',
            'scikit-learn>=0.16.1',
            'networkx>=1.11',
            'pandas>=0.19.0',
            'natsort>=5.0.2'
            # For testing.
            'behave',
            'mock'
        ],
        description='Vectools - A bioinformatics-focused command-line utility for linear algebra, \
        table manipulation, machine leaning, networks/graphs, and more.',
        long_description=long_description,
        platforms='any',
        scripts=['vectools']
    )
