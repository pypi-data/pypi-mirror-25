import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name = 'raspmanager',
    version = '1.0',
    description = "",
    description_file = "README.rst",

    author = 'Yeison Cardona',
    author_email = 'yeisoneng@gmail.com',
    maintainer = 'Yeison Cardona',
    maintainer_email = 'yeisoneng@gmail.com',

    #url = 'http://www.pinguino.cc/',
    url = 'http://yeisoncardona.com/',
    download_url = 'https://bitbucket.org/android-piton/core/downloads',

    packages = find_packages(),
    install_requires = [],

    scripts = [
        "cmd/raspmanager",
        ],

    zip_safe = False,

    include_package_data = True,
    license = 'BSD License',

    classifiers = [
        'Environment :: Web Environment',
    ],
)
