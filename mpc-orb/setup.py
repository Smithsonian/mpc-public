import os
import shutil
import setuptools
from setuptools.command.build_py import build_py as _build_py

# Use the README from src/mpc_orb, *not* the top-level README
with open("src/mpc_orb/README.md", "r") as fh:
    long_description = fh.read()

class build_py(_build_py):
    """ Class to extend the build_py command to include a step that copies JSON schema files
        from the defining directories in mpc-orb, down into the `build` directories
        in preparation for distribution to PyPI.

        MJP: 2024: chatGPT: https://chat.openai.com/c/5a77f06f-9e0d-4211-afad-c6c30bab7de9
    """
    def run(self):
        for dir in ['schema_json','sample_json']:
            # Define source and target directories
            src_dir = os.path.join(os.path.dirname(__file__), dir)
            dst_dir = os.path.join(self.build_lib, 'mpc_orb', dir)
            print(f'src_dir={src_dir} , dst_dir={dst_dir}')
            # Get rid of any existing target directory and contents
            #print(f'removing {dst_dir}',flush=True)
            shutil.rmtree(dst_dir, ignore_errors=True)
            # Copy directory and contents
            #print(f'copying {src_dir}',flush=True)
            shutil.copytree(src_dir, dst_dir)

        super().run()


setuptools.setup(
    name='mpc_orb',
    version='0.2.1',
    long_description=long_description,  
    long_description_content_type="text/markdown",
    author='MJP:MPC',
    author_email='mpayne@cfa.harvard.edu',
    url='https://github.com/Smithsonian/mpc-public',
    install_requires=[
        'jsonschema',
        'numpy',
        'pytest'],
    #packages=setuptools.find_packages(),#where="mpc_orb"),
    #package_data={"": ["schema_json/*.json" , "demo_json/*.json"]},
    packages=setuptools.find_packages(where='src'),
    package_dir={'': 'src'},
    cmdclass={
        'build_py': build_py,
    },
    zip_safe=False)
