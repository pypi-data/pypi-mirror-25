import os
from setuptools import setup, find_packages

# Get the directory that the setup.py script is in.
base_dir = os.path.dirname(os.path.abspath(__file__))

# Gathering metadata for the package.
about = {}
with open(os.path.join(base_dir, 'avail', '__init__.py')) as f:
    for line in f:
        if line.startswith('__'):
            exec(line, about)

# Gather all install_requires values.
install_requires = ['requests>=2.14.0',
                    'colorama>=0.3.9']

# Find all available classifiers at:
# https://pypi.python.org/pypi?%3Aaction=list_classifiers
classifiers = ['Development Status :: 5 - Production/Stable',
               'Environment :: Console',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: Apache Software License',
               'Natural Language :: English',
               'Operating System :: MacOS',
               'Operating System :: Microsoft :: Windows',
               'Operating System :: POSIX',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.4',
               'Programming Language :: Python :: 3.5',
               'Programming Language :: Python :: 3.6',
               'Programming Language :: Python :: Implementation :: CPython',
               'Topic :: Internet',
               'Topic :: Utilities']

# Run the setup() command to build the package.
setup(name=about['__title__'],
      author=about['__author__'],
      author_email=about['__email__'],
      license=about['__license__'],
      version=about['__version__'],
      description='',
      url=about['__url__'],
      packages=find_packages('.', exclude=['.tox', 'tests']),
      install_requires=install_requires,
      zip_safe=False,
      classifiers=classifiers,
      entry_points={'console_scripts': ['avail=avail.cli:main']})
