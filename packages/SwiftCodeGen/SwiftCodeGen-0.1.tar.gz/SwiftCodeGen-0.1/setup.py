from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SwiftCodeGen',
    version='0.1',
    description='A command line utility to generate model and web service classes in Swift programming language.',
    long_description=long_description,
    url='https://github.com/akhilraj-rajkumar/swift-code-gen',
    author='Akhilraj Rajkumar',
    author_email='akhilr46@gmail.com',
    license='Apache License',
    
    py_modules=['swift_gen'],
    install_requires=[
        'Click',
        'mod_pbxproj',
        'enum',
        'stemming',
        'python-dateutil',
        'pathlib',
        'python-string-utils',
    ],
    entry_points='''
        [console_scripts]
        swiftcodegen=swift_gen:cli
    '''
)
