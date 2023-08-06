try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

long_description = ""
with open('README.rst') as f:
	long_description = f.read()

setup(
	name='nway',
	version='3.7',
	author='Johannes Buchner',
	author_email='johannes.buchner.acad@gmx.com',
	packages=['nwaylib'],
	scripts=['nway.py', 'nway-write-header.py', 'nway-explain.py', 'nway-create-fake-catalogue.py', 'nway-create-shifted-catalogue.py', 'nway-calibrate-cutoff.py'],
	url='http://pypi.python.org/pypi/nway/',
	license='AGPLv3 (see LICENSE file)',
	description='Probabilistic Cross-Identification of Astronomical Sources',
	long_description=long_description,
	install_requires=[
		"scipy",
		"numpy",
		"astropy",
		"progressbar-latest",
		"matplotlib",
		"argparse",
		"joblib",
		"healpy",
	],
)


