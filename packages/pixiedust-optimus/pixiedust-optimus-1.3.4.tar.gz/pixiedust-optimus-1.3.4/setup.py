from setuptools import setup, find_packages
setup(name='pixiedust-optimus',
	  version='1.3.4',
	  description='Productivity library for Spark Python Notebook',
	  url='https://github.com/FavioVazquez/pixiedust-optimus',
	  install_requires=['mpld3','lxml','geojson'],
	  author='David Taieb - Favio Vazquez',
	  author_email='david_taieb@us.ibm.com',
	  license='Apache 2.0',
	  packages=find_packages(exclude=('tests', 'tests.*')),
	  include_package_data=True,
	  zip_safe=False
)
