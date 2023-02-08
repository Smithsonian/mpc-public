import setuptools

setuptools.setup(
	name='mpc_orb',
	version='0.0.4',
	description='For the validation and parsing of mpc_orb.json formatted data',
	author='MJP:MPC',
	author_email='mpayne@cfa.harvard.edu',
	url='https://github.com/matthewjohnpayne/mpc_orb',
	install_requires=[
		'jsonschema',
		'numpy',
		'pytest'],
	packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'' : ['mpc_orb/schema_json/*.json']},
	zip_safe=False)

