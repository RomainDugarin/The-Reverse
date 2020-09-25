from setuptools import setup, find_packages
from pkg_resources import parse_requirements

setup_requires = [
    'setuptools>=45.2',
    'discord.py'
]

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

setup(name="The-Reverse",
    version="0.1",
    description="Discord Client",
    url="https://github.com/AlphaCodeCorp/The-Reverse",
    author="AlphaCode",
    author_email="incisiflefufu@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    setup_requires = setup_requires,
    install_requires = install_requires,
    data_files=[('etc')],
    scripts=[])