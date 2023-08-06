from setuptools import setup, find_packages
dependencies =[
]

VERSION = "0.0.2"

setup(
    name = 'folslib',
    packages = ['folslib'],
    version = VERSION,
    description = "Folger's Python Lib",
    author = 'Folger Lun',
    author_email = 'lunbest@hotmail.com',
    url = 'https://github.com/folger/folslib',
    download_url = 'https://github.com/folger/folslib/archive/{}.tar.gz'.format(VERSION), 
    keywords = ['hello', 'world'],
    include_package_data=True,
    requires=dependencies
)
