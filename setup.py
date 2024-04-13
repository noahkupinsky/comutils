
from setuptools import setup, find_packages

setup(
    name='comutils',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'appdirs', 
        'cominfer'
    ],
    entry_points={
        'console_scripts': [
            'comutils=comutils.command:main',
        ],
    },
    author='Your name here',
    author_email='Your email here',
    description='Your description here.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
