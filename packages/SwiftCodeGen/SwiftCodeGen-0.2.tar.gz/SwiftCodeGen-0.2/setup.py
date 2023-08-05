from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='SwiftCodeGen',
    version='0.2',
    description='A command line utility to generate model and web service classes in Swift programming language.',
    long_description=long_description,
    url='https://github.com/akhilraj-rajkumar/swift-code-gen',
    author='Akhilraj Rajkumar',
    author_email='akhilr46@gmail.com',
    license='Apache License',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='Swift code generator, webservice generator, model generator',
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
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    entry_points='''
        [console_scripts]
        swiftcodegen=swift_gen:cli
    '''
)
