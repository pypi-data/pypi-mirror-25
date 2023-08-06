from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hatchet',
    version='0.0.1',
    description='Library for analuzig calling context trees',
    url = 'https://github.com/LLNL/hatchet',
    author = 'Abhinav Bhatele',
    author_email = 'bhatele@llnl.gov',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='',
    packages = ['hatchet'],
)

