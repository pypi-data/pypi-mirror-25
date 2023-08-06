from setuptools import setup

def readme():
	with open('README.md') as f:
		return f.read()

setup(name='key_note',
	  version='0.1',
	  description='notes linked with keywords',
	  long_description=readme(),
	  scripts=['bin/note'],
	  classifiers=[
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python'],
	  url='https://github.com/dvector89/key_note',
	  author='dvector89',
	  author_email='shiliangliang.cas@gmail.com',
	  license='MIT',
	  packages=['key_note'],
	  include_package_data=True)
