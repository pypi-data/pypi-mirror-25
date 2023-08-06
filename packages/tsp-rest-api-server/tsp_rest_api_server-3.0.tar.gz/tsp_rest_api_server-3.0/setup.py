#!/usr/bin/env python

from setuptools import setup, find_packages

setup_requires = []

install_requires = [
    'click==6.7',
    'Eve==0.7.4',
    'Events== 0.2.2',
    'flask<=0.12,>=0.10.1',
    'Flask-PyMongo==0.5.1',
    'itsdangerous==0.24',
    'Jinja2==2.9.6',
    'MarkupSafe==0.23',
    'simplejson==3.11.1',
    'Werkzeug==0.11.15',
]

dev_requires = [
    'mock==2.0.0',
]

mongo_requires = [
    'pymongo==3.5.1',

]

setup(
    name='tsp_rest_api_server',
    version='v3.0',
    author='Marcos Caputo <caputo.marcos@gmail.com>',
    url='https://github.com/caputomarcos/tsp-rest-api-server',
    description="TSP Rest Api Server - Rest Api Server using Dijsktra's algorithm applied to travelling salesman problem.",
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['docs', ]),
    zip_safe=True,
    install_requires=install_requires,
    extras_require={
        'dev': install_requires + dev_requires,
        'mongo': install_requires + mongo_requires,
    },
    license='MIT',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'tsp_rest_api_server = tsp_api.__main__:main',
        ],
    },
    classifiers=[
        'Framework :: Flask',
        'Programming Language :: Python',
    ],
)
