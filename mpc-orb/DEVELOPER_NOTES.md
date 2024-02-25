# mpc-public: Developer Notes

## Defining Schema for MPCORB.DAT

I am deliberately keeping the defining schema for the `mpc_orb.json` format at the top level of mpc-orb. 
This is to emphasize that:
 - (a) the schema are separate from the python code;
 - (b) to maintain a single source of truth for the schema;

Because the defining `mpc_orb.json` files are not in the python `src/..` directory, 
we need to do something with them to make them available to the python code when it is packaged and distributed. 

The chosen solution is to *copy* the JSON-related directories to the `build/lib/mpc_orb/` directory during the *build* process.
This is handled automatically by the `setup.py` script: see [the Local Build section](#local-build) below. 


## Local Development

Work within a branch, etc etc. 

If you want to edit/develop the code within `src/mpc_orb/`, ensure that you create appropriate 
unit tests within the `tests/` directory.

To check that your code will work as expected when distributed, you can run the commands in [the Local Build section](#local-build) below.


### Local Build 

To create a local copy of the build and check whether it works as expected,
we can do the following: 
````
python3 setup.py build_py
python3 setup.py bdist_wheel 
pip install dist/mpc_orb-0.2.1-py3-none-any.whl --force-reinstall
pytest -v tests 
````
N.B. (1) You may need to change the name of the `dist/mpc_orb-***` as appropriate. 

N.B. (2) The `--force-reinstall` is used to ensure that the package is reinstalled, even if it is already installed. 

N.B. (3) The `pytest -v tests` command runs the various unit tests.
If the build & dist-install (above) worked, then the unit-tests should pass. 
Because the unit-tests require JSON files to exist within the `../site-packages/mpc_orb/sample_json/` directory, 
they help to check both that the `sample_json` was copied into the `build` directory, 
and that this was subsequently installed. 

## Pushing to PyPI

### Release Version: setup.py

You probably need to increment the *version* in the repo's setup.py script.
 - E.g. "*mpc_orb/setup.py*"
 - This controls the version number uploaded and made available on PyPI
 - If you don't increment the version (e.g. from 'v0.0.5' to 'v0.0.6') the upload tp PyPI will likely fail

### GitHub Action

The GitHub action is triggered when you manually create a release.  
Here’s a step by step:

 - Go to the repo webpage: https://github.com/Smithsonian/mpc-public
 - In the right pane, click “Releases -> Then click “Draft a new Release”
 - Click Choose a tag -> Type v0.0.6 -> Create New Tag
 - Also type “v0.0.6” as the Release title
 - Optional release notes
 - Click Publish Release -> This triggers the GitHub action to publish to pypi
 - Watch the Actions to make sure it passes: https://github.com/Smithsonian/mpc-public/actions
 - Then check PyPI to make sure the new version is shown: E.g. https://pypi.org/project/mpc-orb/

