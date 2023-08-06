'''PyCRTools instalation file'''

from setuptools import setup, find_packages

setup(name='pycrutils',
      version='0.0.0.dev2',
      description='A set of tools for a application developtment',
      keywords='development',
      url='https://bitbucket.org/code-reapers/pycrutils/overview',
      author='CodeReaper91',
      author_email='codereaper91@gmail.com',
      license='MIT',
      python_requires='>=3',
      packages=find_packages(exclude=["*.test","*.test.*"]),
      test_suite='nose.collector',
      tests_require=['nose'])
