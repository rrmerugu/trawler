from setuptools import setup

dependencies = [p.rstrip('\n') for p in open('requirements/requirements.txt')]

setup(
    name='trawler',
    version='1.1.0',
    packages=['trawler', 'trawler.browsers' ],
    url='https://github.com/invaana/trawler',
    license='',
    author='Ravi RT Merugu',
    author_email='rrmerugu@gmail.com',
    description='A data gathering framework to search and get information from web sources',
    install_requires=dependencies,
)