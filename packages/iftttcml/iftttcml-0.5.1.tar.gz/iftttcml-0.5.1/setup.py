# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import iftttcml

def readme():
    with open('DESCRIPTION.rst', encoding="utf-8") as f:
        return f.read()

setup(
    name='iftttcml',
    version=iftttcml.__version__,
    packages=find_packages(),
    author='penicolas',
    author_email='png1981@gmail.com',
    description='ITFFF: custom maker launcher',
    long_description=readme(),
    install_requires=['metrovlc'],
    url='https://bitbucket.com/penicolas/ifttt-cml',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'iftttcml = iftttcml.iftttcml:main',
        ],
    },
)
