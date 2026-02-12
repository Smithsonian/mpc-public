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

1. **Install dependencies** 
```bash
pip install -r requirements.txt
```

2. **Make a new branch**
3. **Add-to / Alter some documentation**

   E.g. Create / Edit one or more *markdown* files such as [docs/index.md](docs/index.md)

4. **Examine locally**
 - From the project root, run from the command-line: `mkdocs serve --livereload`
 - See [Issue #8478](https://github.com/squidfunk/mkdocs-material/issues/8478) on the addition of `--livereload` argument. Once `mkdocs` solves this issue, it should automatically watch for changes without the `--livereload` flag.
 - Then examine in browser: `http://127.0.0.1:8000/index.html`

5. Push Branch to Repo & Request Review
```bash
git add <some.file>
git commit - m 'some message'
git push 
```

 - Open PR. 
 - Request review.

6. Once approved, you can merge into `main`. The [public version](https://docs.minorplanetcenter.net) will automatically update in the [deploy-docs-public.yml](../.github/workflows/deploy-docs-public.yml) GitHub Action.

7. Navigate to the public site, [docs.minorplanetcenter.net](https://docs.minorplanetcenter.net/), and check results are as desired. 
   (You might need to give it a few seconds to update.)
