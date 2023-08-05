#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = []

test_requirements = [
    'pytest',
]

if __name__ == '__main__':
    setup(
        name='changelogdir',
        version='3.1.0',
        url='https://gitlab.com/carmenbianca/changelogdir',

        author='Carmen Bianca Bakker',
        author_email='carmen@carmenbianca.eu',

        description='Generate a changelog from a directory structure to avoid merge conflicts',
        long_description=open('README.rst').read(),

        package_dir={'': 'src'},
        py_modules=[
            'changelogdir',
        ],

        entry_points={
            'console_scripts': ['changelogdir=changelogdir:main'],
        },

        install_requires=requirements,
        tests_require=test_requirements,

        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3 :: Only',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Documentation',
            'Topic :: Text Processing',
            'Topic :: Text Processing :: Markup',
            'Topic :: Utilities',
        ],
    )
