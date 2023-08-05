from setuptools import setup, find_packages
import sys, os

version = '0.0.7'

setup(name='lotonumber',
      version=version,
      description="show a right number of loto.",
      long_description="""\
show a correct number of loto.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='loto number',
      author='solima',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'numpy',
          'matplotlib',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      loto = lotonumber.loto:main
      miniloto = lotonumber.miniloto:main
      loto6 = lotonumber.loto6:main
      loto7 = lotonumber.loto7:main
      """,
      )
