#!/usr/bin/python3

from setuptools import setup

setup(
    name='wayround_org_webserver',
    version='0.1.2',
    description='homebrewn webserver',
    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='https://github.com/AnimusPEXUS/wayround_org_webserver',
    packages=[
        'wayround_org.webserver'
        ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
        ],
    entry_points={
        'console_scripts': [
            'wrows = wayround_org.webserver.main'
            ],
        }
    )
