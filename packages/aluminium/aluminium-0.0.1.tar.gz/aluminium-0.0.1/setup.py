"""The setup for 'aluminium' python system administration toolkit.

For more details see:
https://github.com/thee-engineer/aluminium
"""

import io

from setuptools import setup, find_packages
from codecs import open as copen
from os import path

from aluminium.help import __version__

CWD = path.abspath(path.dirname(__file__))

with copen(path.join(CWD, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()
    LONG_DESCRIPTION = LONG_DESCRIPTION.replace("\r", "")


def read(*names, **kwargs):
    """Read file contents."""
    with io.open(
        path.join(path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ) as fp:
        return fp.read()


setup(
    name='aluminium',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version=__version__,

    description='System administration toolkit.',
    long_description=LONG_DESCRIPTION,

    # The project's main homepage.
    url='https://github.com/thee-engineer/aluminium',

    # Author details
    author='Alexandru-Paul Copil (thee-engineer)',
    author_email='alexandru.p.copil@gmail.com',

    # Choose your license
    license='GNU General Public License v3 (GPLv3)',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project?
        'Development Status :: 1 - Planning',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',

        # Topics
        'Topic :: System',
        'Topic :: Utilities',

        # Environment
        'Environment :: Other Environment',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Language
        'Natural Language :: English',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',

        # OS
        'Operating System :: Unix',
    ],

    # What does your project relate to?
    keywords='kit system administrator sys-admin sysadmin admin unix tools',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'old', 'tests', 'dist', 'build']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
    },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
        ],
    },
)
