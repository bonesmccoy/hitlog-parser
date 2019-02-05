from setuptools import setup
from setuptools import find_packages

setup(name='hitlog',
      version='0.1',
      description='CLI Hitlog Processor',
      author='Daniele Murroni',
      author_email='daniele.murroni@gmail.com',
      packages=find_packages(exclude=['doc', 'tests*', 'src']),
      install_requires=[
          'Click',
      ],
      entry_points='''
        [console_scripts]
        hitlog=cli:cli
    ''',
      )
