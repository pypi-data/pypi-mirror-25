from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


setup(name='jk_pathpatternmatcher',
	version='0.2017.10.7',
	description='A python module to perform simple pattern matching on paths.',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-pathpatternmatcher',
	download_url='https://github.com/jkpubsrc/python-module-jk-pathpatternmatcher/tarball/0.2017.10.7',
	keywords=['filesystem', 'pattern-matching'],
	packages=['jk_pathpatternmatcher'],
	install_requires=[
	],
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.5',
		'License :: OSI Approved :: Apache Software License'
	],
	long_description=readme(),
	zip_safe=False)

