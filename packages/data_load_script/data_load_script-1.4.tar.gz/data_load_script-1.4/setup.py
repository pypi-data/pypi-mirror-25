from setuptools import setup

setup(name='data_load_script',
		version='1.4',
		description='load the input data from Amazon S3, generate main tables and BOM tables, and upload to Amazon S3',
		url='http://github.com/ghao2',
		author='haoguoxuan',
		author_email='haoguoxuan@gmail.com',
		license='MIT',
		packages=['data_load_script'],
		zip_safe=False)