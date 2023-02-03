import setuptools

setuptools.setup(
	name='mpc_orb',
	version='0.0.3',
	description='For the validation and parsing of mpc_orb.json formatted data',
	author='MJP:MPC',
	author_email='mpayne@cfa.harvard.edu',
	url='https://github.com/matthewjohnpayne/mpc_orb',
	install_requires=[
		'jsonschema',
		'numpy'],
	packages=setuptools.find_packages(),
	zip_safe=False)

