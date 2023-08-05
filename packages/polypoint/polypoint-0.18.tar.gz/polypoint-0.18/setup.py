from setuptools import setup, find_packages, Extension
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='polypoint',
    version='0.18',

    description='A Python 3 package for classifying geolocation data.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/josephacall/polypoint',

    # Author details
    author='Joseph Call',
    author_email='josephacall@gmail.com',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Mathematics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='map determine state for coordinates find point in polygon',
    packages=["polypoint"],
    install_requires=['numpy', 'cython'],
    extras_require={
        'dev': ['check-manifest'],
    },
    package_data={
        'polypoint': ['states.xml', 'utils.pyx'],
    },
)
