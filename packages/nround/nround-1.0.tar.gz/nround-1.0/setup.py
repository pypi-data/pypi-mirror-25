from setuptools import setup

with open('README.txt') as readme:
    long_description = readme.read()

setup(
    name='nround',
    author='Roman Bobrovskiy',
    author_email='romul1988@gmail.com',
    version='1.0',
    packages=['nround'],
    url='https://github.com/usernameisalreadytaken4/nround',
    long_description=long_description,
)