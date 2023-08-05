from setuptools import setup, find_packages

import finance_helper

setup(
        name='finance-helper',
        version=finance_helper.__version__,
        packages=find_packages(),
        description='A utility for Fiance',
        author='caviler',
        author_email='caviler@gmail.com',
        license='BSD',
        url='https://github.com/caviler/finance_helper',
        keywords='finance utility',
        install_requires=['requests', 'pyquery'],
        classifiers=['Development Status :: 3 - Alpha',
                     'Programming Language :: Python :: 2.7',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'License :: OSI Approved :: BSD License'],
)
