'''Setup file for gittools package.
'''
from setuptools import setup, find_packages

setup(
	# Application name:
	name="jtitor_basis",
	# Version number (initial):
	version="0.1.1",
	# Application author details:
	author="jTitor",
	author_email="name@addr.ess",
	# Packages
	packages=find_packages(),
	# Include additional files into the package
	include_package_data=True,
	# Details
	url="http://pypi.python.org/pypi/jtitor_basis/0.1.1/",
	license="MIT",
	description=("Framework for cross-platform scripts that run in stages. "
	"Privately listed since it's not quite done."),
	#long_description=open("readme.md").read(),
	# Dependent packages (distributions)
	install_requires=[
		"colorama",
	],
	entry_points={
		'console_scripts': ['testbasis=app.testbasis:main']
	}
)
