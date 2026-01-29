# docs-public

## Overview

`docs-public` provides a **front door** documentation website, 
[https://docs.minorplanetcenter.net/](https://docs.minorplanetcenter.net/), 
allowing external users a simplified means of accessing and searching 
the MPC's existing documentation pages.

Note that the default location for the documentation is 
[https://smithsonian.github.io/mpc-public/](https://smithsonian.github.io/mpc-public/), 
but https://github.com/Smithsonian/mpc-public/settings/pages has been edited to allow the docs to be served from 
[https://docs.minorplanetcenter.net/](https://docs.minorplanetcenter.net/) instead. 

As we improve the documentation, more details/pages/documentation will be 
consolidated *into* [docs-public](https://smithsonian.github.io/docs-public/), 
but for now, this page primarily serves as a *map into the existing documentation*.


## Setup & Development 

1. **Install mkdocs** 
```bash
pip install mkdocs mkdocs-material mkdocs-jupyter
```

2. **Make a new branch**
3. **Add-to / Alter some documentation**

   E.g. Create / Edit one or more *markdown* files such as [docs/index.md](docs/index.md)

4. **Examine locally**
 - From the project root, run from the command-line: `mkdocs serve`
 - Then examine in browser: `http://127.0.0.1:8000/docs-public`

5. Push Branch to Repo & Request Review
```bash
git add <some.file>
git commit - m 'some message'
git push 
```

 - Open PR. 
 - Request review.

6. **Update the deployed public version.**

 - Update the docs, `mkdocs gh-deploy`
```bash
cd mpc-public/docs-public
mkdocs gh-deploy
```
 - Navigate to site, `https://docs.minorplanetcenter.net/`, and check results are as desired 
   (you might need to give it a few seconds to update)

 
N.B.(1) The WIP git branch does *not* have to be merged for the 
        `mkdocs gh-deploy` step to update the public site. 
        This means that it is possible for the public site to be updated 
        without a PR being opened or a review performed. 

N.B.(2) I assume that the `mkdocs gh-deploy` step could be replaced by 
        some form of automated, post-merge github action. 
 
