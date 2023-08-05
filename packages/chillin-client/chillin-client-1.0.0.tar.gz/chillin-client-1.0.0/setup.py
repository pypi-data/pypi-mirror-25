import sys
from setuptools import setup, find_packages


setup(
    name='chillin-client',
    version='1.0.0',
    description='Chillin AI Game Framework (Python Client)',
    long_description='',
    author='k04la',
    author_email='mdan.hagh@gmail.com',
    url='https://github.com/k04la/Chillin-PyClient',
    keywords='ai game framework chillin',

    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],

    license='MIT',

    install_requires=[
        'koala-serializer==0.5.0',
        'configparser==3.5.0',
        'enum34==1.1.6'
    ],

    packages=find_packages()
)
