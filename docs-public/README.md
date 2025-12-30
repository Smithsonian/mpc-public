# docs-public

## Overview

`docs-public` provides a **front door** documentation website, 
[https://smithsonian.github.io/mpc-public/](https://smithsonian.github.io/mpc-public/), 
allowing external users a simplified means of accessing and searching 
the MPC's existing documentation pages.

As we improve the documentation, more details/pages/documentation will be 
consolidated *into* [docs-public](https://smithsonian.github.io/docs-public/), 
but for now, this page primarily serves as a *map into the existing documentation*.


## Setup & Development 

1. Install mkdocs ... 
```bash
pip install mkdocs mkdocs-material
```

2. Add-to / Alter some documentation 

3. Examine locally 
 - From the project root, run from the command-line: `mkdocs serve`
 - Then examine in browser: `http://127.0.0.1:8000/docs-public`

4. Examine deployed version 
 - Add, Commit & Push (to branch) 
```bash
git add <some.file>
git commit - m 'some message'
git push 
```
 - Update the docs, `mkdocs gh-deploy`
 - Navigate to site, `https://Smithsonian.github.io/mpc-public/` (you might need to give it a few seconds to update)