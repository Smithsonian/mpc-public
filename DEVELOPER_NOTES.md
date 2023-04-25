# mpc-public: Developer Notes

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

