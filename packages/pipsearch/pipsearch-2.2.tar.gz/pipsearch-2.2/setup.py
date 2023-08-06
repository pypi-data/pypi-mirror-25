from setuptools import setup

setup(name="pipsearch",
	  version="2.2",
	  description="Search pypi modules",
	  url="https://github.com/biggydbs/pipsearch",
	  author="Hitesh Jain",
	  author_email="jain.hitesh30695@gmail.com",
	  packages=["pipsearch"],
	  scripts=["bin/api"],
	  download_url="https://github.com/biggydbs/pipsearch/archive/2.tar.gz",
	  install_requires=['Click'],
	  py_modules=["bin/api"],
	  entry_points='''
        [console_scripts]
        pipsearch=bin.api:search
    	''',
	  zip_safe=False)