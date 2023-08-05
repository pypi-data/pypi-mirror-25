'''Setup file for gittools package.
'''
from distutils.core import setup

setup(
	# Application name:
	name="jtitor_gittools",
	# Version number (initial):
	version="0.1.0",
	# Application author details:
	author="jTitor",
	author_email="name@addr.ess",
	# Packages
	packages=["app"],
	# Include additional files into the package
	include_package_data=True,
	# Details
	url="http://pypi.python.org/pypi/jtitor_gittools/0.1.0/",
	license="MIT",
	description="Batches common bulk operations on git repositories, but privately listed since it's not quite done.",
	# long_description=open("README.txt").read(),
	# Dependent packages (distributions)
	#install_requires=[
	#	"flask",
	#],
	entry_points={
		'console_scripts': ['gittools=app.gittools:main']
	}
)
