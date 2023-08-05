from setuptools import find_packages, setup

setup(
	name='nodel',
	version='0.2.12',
	packages=find_packages(),
	url='https://github.com/ary4n/nodel',
	license='MIT',
	author='aryan',
	author_email='alikhaniaryan@live.com',
	description='django project manager',
	keywords='minimal django project manager',
	download_url="https://github.com/ary4n/nodel/archive/0.2.12.tar.gz",
	install_requires=[
		'python-dotenv',
	],
)