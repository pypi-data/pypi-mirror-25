from setuptools import setup
from os import path

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

setup(
    name='denv',
    version='1.1.0',
    author='sloev',
    author_email='jgv@trustpilot.com',
    url='https://github.com/trustpilot/python-denv',
    description='runs commands with env stored in dotfile',
    long_description=read('README.rst'),
    packages=['denv'],
    entry_points={
        'console_scripts': [
            'denv=denv:main',
        ],
    },
    license='MIT'
)
