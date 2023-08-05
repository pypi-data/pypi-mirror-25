import codecs
import sys
from setuptools import setup

VERSION = '1.4.1'

INSTALL_REQUIRES = []
TESTS_REQUIRE = [
    'mock>=2.0.0' if sys.version_info < (3, 3) else None,
    'unittest2>=1.1.0' if sys.version_info < (2, 7) else None,
]

with codecs.open('README.rst', encoding='utf-8') as file:
    README = file.read()

setup(name='see',
      version=VERSION,
      description='dir for humans',
      long_description=README,
      author='Liam Cooke',
      author_email='see@liamcooke.com',
      license='BSD License',
      platforms=['any'],
      url='https://ljcooke.github.io/see/',
      packages=['see'],
      install_requires=list(filter(bool, INSTALL_REQUIRES)),
      test_suite='tests',
      tests_require=list(filter(bool, TESTS_REQUIRE)),
      zip_safe=True,
      keywords='see dir alternative inspect human readable pretty'.split(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: Freely Distributable',
          'License :: OSI Approved :: BSD License',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Software Development',
      ])
