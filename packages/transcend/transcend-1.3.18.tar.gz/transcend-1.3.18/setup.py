#python setup.py sdist upload
from setuptools import setup
setup(
	name='transcend',    # This is the name of your PyPI-package.
	version='1.3.18',                          # Update the version number for new releases
	author='Michael Farrell',
	author_email='mike@transcend.io',
	url='https://github.com/transcend-inc/transcend-sdk-python',
	packages=['transcend', 'transcend/formats'] 
)