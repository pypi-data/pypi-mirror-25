import os
from setuptools import setup

setup(
        name = 'hdv_ncddns',
        packages = ["hdv_ncddns"],
        version = '0.0.1',
        author = 'Alex Hyojun Kim',
        author_email = 'alex@hotdev.com',
        description = ' ',
        license = 'BSD',
        install_requires = [
            'requests',
            'xmltodict',
            'colorama'
            ],
        entry_points = {
            'console_scripts': [
                               'ncddns = hdv_ncddns.__main__:main'
                               ]
            }
      )