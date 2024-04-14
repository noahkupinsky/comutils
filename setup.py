from setuptools import setup, find_packages

setup(
    name='comutils',
    version='0.1',
    packages=find_packages(),
    author='Noah Kupinsky',
    author_email='noah@kupinsky.com',
    description='Utilities for making python packages with CLI',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
