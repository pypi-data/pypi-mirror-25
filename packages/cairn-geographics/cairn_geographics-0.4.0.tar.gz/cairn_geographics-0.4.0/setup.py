from setuptools import setup

setup(name='cairn_geographics',
      version='0.4.0',
      description='Client library for Cairn Geographics library.',
      url='http://www.cairngeographics.com',
      author='Cairn Labs, LLC',
      author_email='sam@cairnlabs.com',
      license='MIT',
      packages=['cairn_geographics'],
      keywords='geography census data gis road distance driving time osm',
      install_requires = [
          'requests',
          'pytest',
          'urllib3',
      ],
      zip_safe=False)
