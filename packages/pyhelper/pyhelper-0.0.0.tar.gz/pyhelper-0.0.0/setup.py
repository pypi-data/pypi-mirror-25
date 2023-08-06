from setuptools import setup, find_packages

import pyhelper

setup(
        name='pyhelper',
        version=pyhelper.__version__,
        packages=find_packages(),
        description='A collection of useful python utilities',
        author='caviler',
        author_email='caviler@gmail.com',
        license='BSD',
        url='https://github.com/caviler/pyhelper',
        keywords='pyhelper python utilities thread lock cache',
        install_requires=['requests', 'pyquery'],
        classifiers=['Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'License :: OSI Approved :: BSD License'],
)
