from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='pypartial',
	version='1.0',

	description='Use partial function application in Python',
	long_description=long_description,
	url='https://pypi.python.org/pypi/pypartial',
	author='Akif Patel',
	author_email='akifpatel@supernovaapps.com',
	license='Apache 2.0',
	
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 3',
		'Topic :: Software Development :: Libraries :: Python Modules',
	],
	
	keywords=['python', 'functional programming', 'library', 'notation'],
	packages=['pypartial']
)
