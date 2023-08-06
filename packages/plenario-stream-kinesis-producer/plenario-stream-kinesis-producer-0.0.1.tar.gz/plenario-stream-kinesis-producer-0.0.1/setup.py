#!/usr/bin/env python3

import codecs
import os
from setuptools import setup


source = os.path.join(os.path.dirname(__file__), 'requirements.txt')
requirements = [l for l in codecs.open(source, mode='r', encoding='utf-8')
                if 'git' not in l]
readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(
    name='plenario-stream-kinesis-producer',
    version='0.0.1',
    description='Converts Plenario Stream Core signals into kinesis records',
    long_description=readme,
    url='https://github.com/UrbanCCD-UChicago/plenario-stream-kinesis-producer',
    author='Jesus Bracho',
    author_email='jbracho@uchicago.edu',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='plenario',
    install_requires=requirements,
    dependency_links=[
        'git+git://github.com/UrbanCCD-UChicago/plenario-core.git@\
        master#egg=plenario_core',
        'git+git://github.com/UrbanCCD-UChicago/plenario-stream-core.git@\
        pypi#egg=plenario_stream_core',
    ],
    python_requires='>=3.6',
    packages=[
        'plenario_stream_kinesis_producer',
    ],
)
