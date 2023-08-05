
from setuptools import setup

def readme():
	with open('README.rst') as f:
		return f.read()

setup(
	name='tweetypy',
	version='1.0.0rc6',
	description='Bird song analysis tools',
	long_description=readme(),
	classifiers=[
		'Development Status :: 3 - Alpha',
		'License :: OSI Approved :: MIT License',
		'Intended Audience :: Science/Research',
		'Programming Language :: Python :: 3',
		'Topic :: Multimedia :: Sound/Audio :: Analysis',
		'Topic :: Scientific/Engineering :: Visualization'
	],
	url='http://jessemcclure.org',
	author='Jesse McClure',
	author_email='jmcclure@broadinstitute.org',
	license='MIT',
	packages=['tweetypy'],
	package_data={'tweetypy': ['*.yaml']},
	install_requires=['numpy', 'scipy', 'pyYAML', 'PyQt5' ],
	python_requires='>=3',
	entry_points={'console_scripts': ['tweetypy=tweetypy:main']},
	include_package_data=True,
	zip_safe=False)
