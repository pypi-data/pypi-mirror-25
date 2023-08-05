import os
from setuptools import find_packages, setup

requirements = [
    'requests',
    'ansicolors',
    'progressbar2',
    'termcolor',
    'colorama',
]

# pycrypto and paramiko are optional dependencies

if os.name == 'posix':
    requirements.append('sh')

setup(name="mcommons",
    install_requires=requirements,
    version= "1.0",
    description="Some common utility methods I use often",
    author="Moshe Immerman",
    author_email='name.surname@gmail.com',
    platforms=["any"],
    license="BSD",
    url="http://github.com/Moshe-Immerman/python-commons",
    packages=['commons']
)
