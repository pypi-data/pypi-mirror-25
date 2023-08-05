
# https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup

setup(name='jawiki',
      version='1.4.0',
      description='A Pythonic wrapper for the Japanese Wikipedia API',
      url='http://github.com/tex2e/jawiki',
      author='tex2e',
      author_email='mnfeconicu41@gmail.com',
      license='MIT',
      packages=['jawiki'],
      install_requires=[
          'wikipedia',
      ],
      zip_safe=False)
