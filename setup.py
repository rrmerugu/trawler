from setuptools import setup

# dependencies = [p.rstrip('\n') for p in open('requirements/requirements.txt')]

setup(
    name='trawler',
    version='1.3.6',
    packages=['trawler', 'trawler.browsers', 'tests' ],
    url='https://github.com/rrmerugu/trawler',
    license='',
    author='Ravi RT Merugu',
    author_email='rrmerugu@gmail.com',
    description='A data gathering framework to search and get information from web sources',
    install_requires=[
        'cssselect',
        'lxml',
        'selenium',
        'six',
        'beautifulsoup4',
        'requests',
        'user-agent'
    ],
)