import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mpc_orb',
    version='0.1.1',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='MJP:MPC',
    author_email='mpayne@cfa.harvard.edu',
    url='https://github.com/matthewjohnpayne/mpc_orb',
    install_requires=[
        'jsonschema',
        'numpy',
        'pytest'],
    packages=setuptools.find_packages(),#where="mpc_orb"),
    package_data={'': ['mpc_orb/schema_json/*.json']},
    zip_safe=False)
