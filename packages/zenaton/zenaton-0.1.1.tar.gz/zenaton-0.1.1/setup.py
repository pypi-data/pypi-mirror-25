"""
Zenaton client library
"""
from __future__ import absolute_import, print_function, unicode_literals

from io import open
import os

from setuptools import find_packages, setup


def read(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    with open(path, encoding='utf-8') as f:
        return f.read()


setup(
    name='zenaton',
    version='0.1.1',
    description='Zenaton client library',
    long_description=read('README.rst') + '\n' + read('CHANGELOG.rst'),
    keywords='workflow tasks queue orchestration scheduling',
    url='https://zenaton.com/',
    author='Zenaton',
    author_email='contact@zenaton.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries',
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*',
    install_requires=[
        'docopt',
        'requests',
        'six',
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'zenaton_init = zenaton.scripts.init:main',
            'zenaton_slave = zenaton.scripts.slave:main',
        ],
    },
)
