from distutils.core import setup

from setuptools import find_packages

setup(
    name='jsonapidb',
    packages=find_packages(exclude=['test*']),
    version='0.1.5',
    description='json api interface for mongodb',
    author='prototype-organisation',
    author_email='beczkowb@gmail.com',
    url='https://github.com/prototype-project/jsonapidb',
    download_url='https://github.com/prototype-project/prototype/archive/0.1.5.tar.gz',
    keywords=['jsonapi', 'nosql', 'mongodb', 'database'],
    classifiers=[],
)
