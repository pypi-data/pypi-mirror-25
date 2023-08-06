
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='testrailrobot',

    version='0.9.0',

    description='Package for uploading test results from Robot Framework to TestRail.',
    long_description=long_description,

    url='https://github.com/taneltorn/testrailrobot',

    author='Tanel Torn',
    author_email='tanel.torn@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='testrail robot-framework',

    packages=find_packages(exclude=['docs', 'tests']),

)
