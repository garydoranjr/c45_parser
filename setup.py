try:
    from setuptools import setup
    setup  # quiet "redefinition of unused ..." warning from pyflakes
    # arguments that distutils doesn't understand
    setuptools_kwargs = {
        'install_requires': [
          ],
        'provides': ['c45_parser'],
        }
except ImportError:
    from distutils.core import setup
    setuptools_kwargs = {}

setup(name='c45_parser',
      version="1.0",
      description=(
        'A c4.5 data file parser see '
        'http://www.cs.washington.edu/dm/vfml/appendixes/c45.htm.'
      ),
      author='Gary Doran',
      author_email='gbd6@case.edu',
      url='https://github.com/cwru-compilers/regex_compiler',
      packages=['c45_parser'],
      platforms=['unix'],
      scripts=['bin/c45_to_matlab'],
      **setuptools_kwargs
)

