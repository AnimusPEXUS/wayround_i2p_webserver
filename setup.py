#!/usr/bin/python3

from setuptools import setup

setup(
    name='wayround_i2p_webserver',
    version='0.3',
    description='homebrewn webserver',
    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='https://github.com/AnimusPEXUS/wayround_i2p_webserver',
    install_requires=[
        'wayround_i2p_utils',
        'wayround_i2p_socketserver',
        'wayround_i2p_wsgi'
        ],
    packages=[
        'wayround_i2p.webserver',
        'wayround_i2p.webserver.modules',
        ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)'
        ],
    entry_points={
        'console_scripts': [
            'wrows = wayround_i2p.webserver.main:main'
            ],
        }
    )
