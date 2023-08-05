from distutils.core import setup

NAME = 'LibML'
AUTHOR = 'Austen Schunk'
EMAIL = 'aschunk4@gmail.com'
DESCRIPTION = 'A collection of modules in python that can be used for machine learning'
VERSION = '0.1.03'
PACKAGES = ['libml', 'libml.Classification', 'libml.Utilities']
LICENSE = 'MIT License'

setup(
	name = NAME,
	author = AUTHOR,
	author_email = EMAIL, 
	version = VERSION,
	description = DESCRIPTION,
	packages = PACKAGES,
	license = LICENSE,
	)
