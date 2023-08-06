from setuptools import setup, find_packages
from os.path import join, dirname

from hobbit import __version__ as version

setup(
    name='hobbit',
    version=version,
    packages=find_packages(),
    author='acrius',
    author_email='acrius@mail.ru',
    url='https://github.com/acrius/hobbit',
    description='',
    license='MIT',
    keywords='',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    include_package_data=True,
    include_packages_data=True,
    install_requires=[
        'beautifulsoup4'
    ]
)
