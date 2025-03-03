# mpc-public: Developer Notes

## Developing locally 

Before pushing the new version to `PyPI` you may want to develop and test the new code on your local machine.
```bash
# Create a new conda environment
conda create -n mpc-orb-public python=3.11
conda activate mpc-orb-public
cd mpc_orb
python3 -m pip install -e .'[test]'
```

## Pushing to PyPI

### Release Version: pyproject.toml

You need to increment the *version* in `pyproject.toml`.
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

