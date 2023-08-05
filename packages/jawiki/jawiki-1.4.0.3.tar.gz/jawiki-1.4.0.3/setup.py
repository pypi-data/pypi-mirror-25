
# https://python-packaging.readthedocs.io/en/latest/minimal.html
from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='jawiki',
      version='1.4.0.3',
      description='A Pythonic wrapper for the Japanese Wikipedia API',
      long_description=readme(),
      url='http://github.com/tex2e/jawiki',
      author='tex2e',
      author_email='mnfeconicu41@gmail.com',
      license='MIT',
      packages=['jawiki'],
      install_requires=[
          'wikipedia',
      ],
      include_package_data=True,
      zip_safe=False)
