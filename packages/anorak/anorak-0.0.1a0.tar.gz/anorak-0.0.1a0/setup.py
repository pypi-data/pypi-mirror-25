from distutils.core import setup
from setuptools import find_packages

setup(
    name='anorak',
    version='0.0.1-alpha',
    author='Andreas Dewes - 7scientists',
    author_email='andreas@7scientists.com',
    license='BSD-4',
    entry_points = {
        'console_scripts': ['anorak=anorak.cli.main:anorak'],
    },
    url='https://github.com/7scientists/anorak',
    packages=find_packages(),
    package_data={'': ['*.ini']},
    include_package_data=True,
    install_requires=['six'],
    zip_safe=False,
    description='A data anonymiaztion toolkit for Python.',
    long_description="""A data anonymization toolkit for Python. 
"""
)
