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

The site is built with [**Quarto**](https://quarto.org). Markdown pages and
Jupyter notebooks under `docs/` are rendered to a static site; the Quarto
project config is [`docs/_quarto.yml`](docs/_quarto.yml).

1. **Install dependencies**
   - Install the **Quarto CLI** (standalone, not pip): see
     <https://quarto.org/docs/get-started/>. Check with `quarto --version`.
   - Install the Python bits Quarto's Jupyter engine needs to read the notebooks:
     ```bash
     pip install -r requirements.txt
     ```
     (Notebooks are **not executed** at build time — `execute: false` in
     `_quarto.yml` — so their stored outputs are rendered as-is.)

2. **Make a new branch**
3. **Add-to / Alter some documentation**

   E.g. Create / Edit one or more *markdown* files such as [docs/index.md](docs/index.md)

4. **Examine locally**
 - From the `docs` directory, run a live-reloading preview server:
   ```bash
   cd docs && quarto preview
   ```
   It opens a browser tab (e.g. `http://localhost:4321`) and reloads on save.
 - Or do a one-off build and open the result:
   ```bash
   cd docs && quarto render   # outputs to docs/_site
   ```
 - Notebook tutorials get a "Download this notebook" button and their raw
   `.ipynb` files are copied to `/downloads/notebooks/` by the post-render step
   ([docs/scripts/copy-notebooks.sh](docs/scripts/copy-notebooks.sh)); these
   root-relative links resolve under `quarto preview` and on the live site (but
   not when opening `_site/index.html` directly over `file://`).

5. Push Branch to Repo & Request Review
```bash
git add <some.file>
git commit -m 'some message'
git push 
```

 - Open PR. 
 - Request review.

6. Once approved, you can merge into `main`. The [public version](https://docs.minorplanetcenter.net) will automatically update in the [deploy-docs-public.yml](../.github/workflows/deploy-docs-public.yml) GitHub Action.

7. Navigate to the public site, [docs.minorplanetcenter.net](https://docs.minorplanetcenter.net/), and check results are as desired. 
   (You might need to give it a few seconds to update.)
