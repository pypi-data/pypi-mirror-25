# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

exec(open('fastqmetrics/version.py').read())

setup(
    name='fastqmetrics',
    version=__version__,
    description='Het hoeft voor ',
    long_description=open(path.join(here, "README.rst")).read(),
    url='https://github.com/wdecoster/fastqmetrics',
    author='Wouter De Coster',
    author_email='decosterwouter@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='nanopore sequencing processing',
    packages=find_packages(),
    install_requires=[
        'nanoget>=0.14.0'],
    package_data={'fastqmetrics': []},
    package_dir={'fastqmetrics': 'fastqmetrics'},
    include_package_data=True,
    entry_points={
        'console_scripts': ['fastqmetrics=fastqmetrics.fastqmetrics:main', ]}
)
