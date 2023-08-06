from setuptools import setup

setup(
    name='python-pstore',
    version='0.9',
    packages=['pythonpstore',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    install_requires=['boto3', 'botocore'],
    tests_requires=['nose2', 'mock'],
    test_suite='nose2.collector.collector',
)
