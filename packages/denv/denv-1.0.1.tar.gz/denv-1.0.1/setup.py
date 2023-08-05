from setuptools import setup
from os import path

setup(
    name='denv',
    version='1.0.1',
    author='sloev',
    author_email='jgv@trustpilot.com',
    url='https://github.com/trustpilot/denv',
    description='runs commands with env stored in dotfile',
    packages=['denv'],
    entry_points={
        'console_scripts': [
            'denv=denv:main',
        ],
    },
    license='MIT'
)
