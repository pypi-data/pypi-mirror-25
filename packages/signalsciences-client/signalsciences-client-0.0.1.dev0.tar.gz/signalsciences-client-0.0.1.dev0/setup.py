from distutils.core import setup
from setuptools import find_packages

setup(
    name='signalsciences-client',
    version='0.0.1.dev0',
    author='Matthew Aynalem',
    author_email='maynalem@gmail.com',
    packages=find_packages('signalsciences'),
    package_dir={'': 'signalsciences'},
    url='https://github.com/mayn/signalsciences-client',
    license='MIT',
    description='signalsciences-client - a python client for signalsciences API',
    long_description=open('README.rst').read(),
    install_requires=[
    ],
)
