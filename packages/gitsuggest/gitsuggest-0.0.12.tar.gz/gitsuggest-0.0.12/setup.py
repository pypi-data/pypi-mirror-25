#!/usr/bin/env python
from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst')) as f:
    long_description = f.read()


def _post_install():
    """Post installation nltk corpus downloads."""
    import nltk
    nltk.download('words')
    nltk.download('stopwords')


class PostDevelop(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        self.execute(_post_install, [], msg='Running post installation tasks')


class PostInstall(install):
    """Post-installation for production mode."""
    def run(self):
        install.run(self)
        self.execute(_post_install, [], msg='Running post installation tasks')


setup(
    # Name of the module
    name='gitsuggest',

    # Details
    version='0.0.12',
    description='A tool to suggest github repositories based on the' +
                ' repositories you have shown interest in.',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/csurfer/gitsuggest',

    # Author details
    author='Vishwas B Sharma',
    author_email='sharma.vishwas88@gmail.com',

    # License
    license='MIT',
    packages=['gitsuggest'],
    # NOTE: Package data to be included both in MANIFEST.in and here for sdist
    # to consider it to put in package (MANIFEST) and for setuptools to copy
    # it over (package_data).
    package_dir={'gitsuggest': 'gitsuggest'},
    package_data={'gitsuggest': ['res/*.template', 'gitlang/*.txt']},
    entry_points={
        'console_scripts': [
            'gitsuggest=gitsuggest.commandline:main',
        ],
    },
    test_suite='tests',
    keywords='github repository suggestion',
    classifiers=[
        # Intended Audience.
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        # License.
        'License :: OSI Approved :: MIT License',
        # Project maturity.
        'Development Status :: 3 - Alpha',
        # Operating Systems.
        'Operating System :: POSIX',
        # Supported Languages.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        # Topic tags.
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['gensim', 'PyGithub', 'nltk', 'crayons'],
    cmdclass={
        'develop': PostDevelop,
        'install': PostInstall
    })
