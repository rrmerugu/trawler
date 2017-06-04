from distutils.core import setup

setup(
    name='trawler',
    version='1.0.0',
    packages=['trawler',
              'trawler.db',
              'trawler.browsers',
              'trawler.server',
              'tests'
              ],
    url='https://github.com/invaana/trawler',
    license='',
    author='Ravi RT Merugu',
    author_email='rrmerugu@gmail.com',
    description='This is a data aggregation framework for scouting and aggregating Scientific Data. '
)