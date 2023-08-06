#python setup.py sdist upload
from setuptools import setup
setup(
	name='transcend',    # This is the name of your PyPI-package.
	version='1.3.3',                          # Update the version number for new releases
	packages=['transcend', 'transcend/formats'] 
)