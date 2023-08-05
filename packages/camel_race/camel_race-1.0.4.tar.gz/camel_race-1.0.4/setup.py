#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='camel_race',
      version='1.0.4',
      description='Camel Race ascii game',
      author='Ibrahim Menem',
      author_email='ibrahimmenem@gmail.com',
      url='https://dummystack.com',
      packages=find_packages(),
      install_requires=['enum34'],
      data_files = [('', ['games/camels_race/config.json'])],
      entry_points={
        'console_scripts': [
            'camel_race=games.play:main',
        ],
       }

     )
