from setuptools import setup
from os import path


with open(path.join(path.abspath(path.dirname(__file__)), 'denv/__version__')) as f:
    version = f.readlines()[0]


setup(
    name='denv',
    version=version,
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
