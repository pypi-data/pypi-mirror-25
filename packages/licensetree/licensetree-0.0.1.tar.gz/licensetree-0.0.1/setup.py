from setuptools import setup
from licensetree import __version__

__version__ = list(map(str, __version__))

setup(name='licensetree',
      version='.'.join(__version__),
      description='License Tree Generator for Python Projects',
      url='http://github.com/theSage21/licensetree',
      author='Arjoonn Sharma',
      author_email='arjoonn.94@gmail.com',
      packages=['licensetree'],
      entry_points={'console_scripts': ['licensetree=licensetree.cli:main']},
      keywords=['licensetree', 'license', 'mapping', 'dependeicies'],
      zip_safe=False)
