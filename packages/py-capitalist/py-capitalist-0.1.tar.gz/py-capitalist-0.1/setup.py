# coding: utf-8
from setuptools import setup

import capitalist


with open('README.rst') as file:
    long_description = file.read()

setup(
    name='py-capitalist',
    url='https://github.com/Stranger6667/py-capitalist',
    version=capitalist.__version__,
    packages=['capitalist'],
    license='MIT',
    author='Dmitry Dygalo',
    author_email='dadygalo@gmail.com',
    maintainer='Dmitry Dygalo',
    maintainer_email='dadygalo@gmail.com',
    keywords=['capitalist', 'api', 'client', 'payments'],
    description='Python client library for Capitalist API',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    include_package_data=True,
    install_requires=['requests', 'pycrypto'],
)
