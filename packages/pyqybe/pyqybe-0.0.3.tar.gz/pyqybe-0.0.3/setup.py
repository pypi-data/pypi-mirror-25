import re

from setuptools import setup


def version():
    version_file_name = "pyqybe/__init__.py"
    with open(version_file_name, 'rt') as version_file:
        version_file_content = version_file.read()

        version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
        match = re.search(version_regex, version_file_content, re.M)
        if match:
            return match.group(1)
        else:
            raise RuntimeError("Unable to find version string in %s." % (version_file_name,))


setup(name='pyqybe',
      version=version(),
      author='Eryk Humberto Oliveira Alves',
      author_email='erykwho@gmail.com',
      url='https://github.com/otrabalhador/pyqybe/',
      packages=['pyqybe'],
      keywords='python query sql builder pyqybe',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: PL/SQL',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Scientific/Engineering :: Mathematics',
          'Operating System :: POSIX',
      ],
      test_suite="pyqybe.tests",)
