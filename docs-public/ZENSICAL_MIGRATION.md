# Porting `docs-public` from MkDocs 1.x to Zensical — Assessment

*Compiled 2026-09-08 on branch `zensical-port`. This is a decision/planning
document, not an executed migration — no build files have been changed.*

## TL;DR / verdict

Zensical **reads our existing `mkdocs.yml` natively** and would carry over almost
everything we use — the Material look (via the `classic` theme variant), the
`search` plugin, all our `pymdownx.*`/`admonition`/`toc`/`tables`/`attr_list`
extensions, `extra_css`/`extra_javascript`, our `nav`, and even our
`overrides/main.html` template override. The command mapping is trivial
(`mkdocs serve`→`zensical serve`, `mkdocs build`→`zensical build`).

**But there is one hard blocker: `mkdocs-jupyter` is not supported by Zensical,
with no scheduled implementation date** (confirmed by the Zensical maintainer as
of 2026-08). Zensical does **not** load arbitrary third-party MkDocs plugins — it
ships native re-implementations of a fixed list of 15 plugins, and mkdocs-jupyter
is not among them (it sits un-started in the public backlog). That plugin renders
**all 47 of our tutorial notebooks** and provides the `page.nb_url` value our
`overrides/main.html` uses for the "Download Notebook" button.

**Recommendation: do not port yet.** The notebook tutorials are the single most
valuable part of the site and there is no drop-in replacement for how they are
built. Options, in preference order, are in [§5](#5-decision-options). If/when we
do port, the concrete steps are in [§3](#3-concrete-port-plan) and the required
README/CLAUDE.md edits are in [§4](#4-documentation-instruction-updates).

**Zensical is not the only option.** Because the notebook blocker is specific to
Zensical (the `mkdocs-jupyter` *plugin* itself is actively maintained — v0.26.3,
Apr 2026 — it is only Zensical that refuses to load third-party plugins),
[§6](#6-alternatives-to-zensical-with-native-notebook-support) evaluates the
other realistic paths that *do* render notebooks: staying on MkDocs 1.x, and the
scientific-docs generators Quarto, Jupyter Book/MyST, and Sphinx (+ myst-nb /
nbsphinx).

---

## 1. Why this is on the table

- **MkDocs 2.0** is a ground-up rewrite that *removes plugin support*, breaks the
  Material theme, changes config from YAML to TOML with no auto-migration, and has
  no license and a closed contribution model.
  ([mkdocs-material blog, 2026-02-18](https://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/))
- **MkDocs 1.x** is effectively unmaintained (no security guarantees).
- The Material for MkDocs team's answer is **Zensical** — a new Rust+Python static
  site generator marketed as a "drop-in replacement for MkDocs 1.x."
  ([announcement, 2025-11-05](https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/))

So the medium-term pressure is real, but Zensical is **pre-1.0 (currently
v0.0.60)** and only a *partial* drop-in today.

---

## 2. Component-by-component compatibility

Our current stack is small (`requirements.txt` = `mkdocs`, `mkdocs-material`,
`mkdocs-jupyter`; plus `mkdocstrings[python]` installed only in the RTD build,
where it appears vestigial — it is not in `mkdocs.yml`'s `plugins:`).

| Our `docs-public` component | Zensical status | Action needed |
|---|---|---|
| `mkdocs.yml` (YAML config) | Read natively; `zensical.toml` optional, not required | none (keep YAML) |
| `theme: material` + `features` | Reproduced by `theme.variant: classic`; "complete Material settings surface" supported (per-feature matrix not published — verify by testing) | add `variant: classic`; test each feature |
| `theme.custom_dir: overrides` | Supported (path relative to config) | none |
| `overrides/main.html` (`{% extends "base.html" %}`, `{% block content %}`, `{% include ".icons/material/download.svg" %}`) | Supported — **but engine is now MiniJinja, not Jinja**; overrides built for Material ≥ 9.6.18 work unchanged | verify; **the `page.nb_url` reference dies with mkdocs-jupyter** (see below) |
| `plugins: search` | Native support (since 0.0.3) | none |
| `plugins: mkdocs-jupyter` | **NOT supported; no ETA** | **BLOCKER — replace notebook pipeline** |
| `markdown_extensions` (admonition, toc, tables, attr_list, pymdownx.highlight/inlinehilite/snippets/superfences) | All supported (Python-Markdown + strong PyMdown support) | none |
| `extra_css` (3 files) | Works unchanged with `classic` variant | none |
| `extra_javascript` (`force-ipynb-download2.js`) | Works unchanged (static asset) | logic may change — see notebook workaround |
| GitHub Action `deploy-docs-public.yml` (`mkdocs build … -d site` → Pages) | `mkdocs build` → `zensical build`; **note `-d/--site-dir` flag is unsupported** — output goes to `site/` by default | rewrite build step |
| Root `.readthedocs.yaml` (`mkdocs build …`) | same | rewrite or retire |
| `mkdocs gh-deploy` (referenced in CLAUDE.md) | **Not provided by Zensical** | remove reference; we already deploy via Action, not gh-deploy |

**Net:** everything is green except the notebook plugin — which unfortunately
powers the whole `tutorials/` section.

### The notebook blocker in detail
`mkdocs-jupyter` gives us three things we rely on:
1. Automatic rendering of `docs/**/*.ipynb` into HTML pages in the `nav`.
2. `execute: false` / `include_source: true` behavior.
3. The `page.nb_url` template variable, used in `overrides/main.html` to render the
   "Download Notebook" button.

None of these exist in Zensical. The community workaround (from
[zensical/zensical#52](https://github.com/zensical/zensical/issues/52)) is a
**post-build nbconvert script**: after `zensical build`, convert each
`docs/**/*.ipynb` to styled HTML written into `site/`, and point markdown links at
the resulting `.html`. There is no `page.nb_url` equivalent — notebook URLs must
be managed by hand. This is a real chunk of custom tooling to build, test, and
maintain, and it would change how the tutorials appear in the nav.

---

## 3. Concrete port plan (when we decide to go)

This is what a full port would touch. **Not applied in this branch.**

1. **`docs-public/requirements.txt`**
   ```diff
   - mkdocs
   - mkdocs-material
   - mkdocs-jupyter
   + zensical
   + nbconvert>=7   # for the notebook post-build conversion script
   + nbformat
   ```

2. **`docs-public/mkdocs.yml`** — keep as-is except:
   ```diff
     theme:
       name: material
   +   variant: classic          # reproduce the Material look under Zensical
       custom_dir: overrides
     plugins:
       - search
   -   - mkdocs-jupyter:
   -       execute: false
   -       include_source: true
   ```
   (Notebook rendering moves out of the config into the post-build step.)

3. **`docs-public/overrides/main.html`** — the `{% if page.nb_url %}` button no
   longer works (no mkdocs-jupyter). Either drop it or re-implement the download
   affordance in the nbconvert template. Verify the remaining override against
   MiniJinja (should be fine for current Material base templates).

4. **New: `docs-public/scripts/convert_notebooks.py`** — post-build nbconvert
   pass that renders the 47 notebooks to HTML into `site/`, styled to match, and
   rewrites/points the tutorial links. (Model on the script in issue #52.)

5. **`.github/workflows/deploy-docs-public.yml`** — build step becomes:
   ```diff
   - - name: Build site
   -   run: mkdocs build -f docs-public/mkdocs.yml -d site
   + - name: Build site
   +   run: |
   +     cd docs-public
   +     zensical build            # outputs to docs-public/site (no -d flag)
   +     python scripts/convert_notebooks.py
   ```
   then upload `docs-public/site` as before. (Everything else — Pages config,
   artifact upload, deploy — is unchanged.)

6. **Root `.readthedocs.yaml`** — either update its `commands:` to
   `pip install zensical … && cd docs-public && zensical build --… && python
   scripts/convert_notebooks.py`, or retire the RTD build if the GitHub Pages
   Action is our only production target (worth confirming whether RTD is actually
   used — it also pulls in `mkdocstrings[python]`, which is not in `mkdocs.yml`).

7. **Housekeeping (do regardless):** remove the stray build dirs `docs-public/site`
   and the nested `docs-public/docs-public/site` (untracked local artifacts; the
   root `/site` gitignore rule is anchored and doesn't cover the nested one). Add a
   `docs-public/.gitignore` with `site/`.

---

## 4. Documentation / instruction updates

### `docs-public/README.md`
- **§Setup step 4** — replace the local-preview command:
  ```diff
  - - From the project root, run from the command-line: `mkdocs serve --livereload`
  - - See [Issue #8478](https://github.com/squidfunk/mkdocs-material/issues/8478) on the addition of `--livereload` …
  + - From the `docs-public` directory, run: `zensical serve`
  +   (auto-reloads on change; use `-a 127.0.0.1:8000` to set the address).
  + - Notebook tutorials are rendered by a post-build step, so to preview them
  +   run `zensical build && python scripts/convert_notebooks.py` and open `site/`.
  ```
  (The `--livereload` note and Issue #8478 caveat are mkdocs-specific and should
  go — Zensical's `serve` auto-reloads.)
- **§Setup step 6** — the sentence about the deploy Action stays, but drop any
  implication that `mkdocs` is the builder.
- Add an **Install** note: `pip install -r requirements.txt` still works; call out
  that the builder is now `zensical` and Python ≥ 3.10 is required.

### `CLAUDE.md` (repo root, "docs-public (Documentation Site)" section)
- Replace the three commands:
  ```diff
  - pip install mkdocs mkdocs-material mkdocs-jupyter
  + pip install -r docs-public/requirements.txt   # zensical + nbconvert

  - mkdocs serve
  + zensical serve                                 # from docs-public/

  - # Deploy to public site
  - mkdocs gh-deploy
  + # Deploy: push to main; the deploy-docs-public.yml Action runs
  + # `zensical build` + scripts/convert_notebooks.py and publishes to Pages.
  ```
- Add a line to the "Tutorial Notebook Conventions" note: notebooks are no longer
  rendered by an mkdocs plugin but by a post-build nbconvert script; the
  `execute: false` behavior is preserved by that script (notebooks are not
  executed at build time).

---

## 5. Decision options

1. **Stay on MkDocs 1.x + Material for now (recommended).** The site builds and
   deploys fine today. Revisit when either (a) Zensical implements mkdocs-jupyter
   / its third-party module system (planned "early 2026" but the notebook plugin
   is explicitly un-started), or (b) we are forced off 1.x by a real security
   issue. Lowest cost, no user-visible change.
2. **Port everything except notebooks now; keep notebooks on the nbconvert
   workaround.** Full Zensical adoption per §3. Cost: build and maintain
   `convert_notebooks.py`, lose `page.nb_url`, re-verify nav/appearance for 47
   notebooks. Buys us off the unmaintained 1.x sooner.
3. **Hybrid / wait-and-see:** track [backlog #9](https://github.com/zensical/backlog/issues/9)
   and the [ZAP-007 module system](https://zensical.org/spark/proposals/zap-007-module-system/);
   do the low-risk housekeeping (§3.7) and the `variant: classic` test on a branch
   now so we're ready to flip quickly once mkdocs-jupyter lands.

My recommendation is **option 1 now + the option 3 prep** (housekeeping + a
throwaway `zensical serve` smoke test to confirm theme/extension parity), because
the notebook pipeline is both the most valuable and the only genuinely blocked
part of the port.

---

## 6. Alternatives to Zensical with native notebook support

Zensical is the Material team's chosen successor, but it is not the only way to
stay off unmaintained MkDocs 1.x while keeping our 47 notebooks. The important
correction to the framing above: **`mkdocs-jupyter` is actively maintained**
(v0.26.3, Apr 2026, Python 3.9–3.12) — the plugin is fine; only *Zensical*
declines to load it. So the realistic field is:

| Candidate | Native `.ipynb` | No-execute mode | Markdown-reuse friction | Material-like theme | Maintenance (2026) | GH Pages | Migration effort |
|---|---|---|---|---|---|---|---|
| **Stay: MkDocs 1.x + Material + mkdocs-jupyter** | Yes (`page.nb_url`) | `execute: false` | **None** | **Already Material** | Core frozen; Material in maintenance (reported ~EOL Nov 2026); **plugin active** | `gh-deploy` / our Action | **Zero** (tail risk) |
| **Quarto 1.9/1.10** | Yes | **Default** (no-exec) | Medium (Pandoc; `!!!`→callouts, attr_list, tabs) | Clean, not Material | Strong (Posit); Quarto 2 Rust rewrite pending late-2026 | Official Action | **Medium** |
| **Jupyter Book v2 / mystmd 1.10** | Yes | **Default** (opt-in exec) | Medium (MyST; `!!!`→`:::`) | Clean, not Material | Active; still closing v1 parity gaps | `myst init --gh-pages` | **Medium** |
| **Sphinx + myst-nb 1.3** | Yes | `nb_execution_mode="off"` | Medium (MyST) | **sphinx-immaterial = closest to Material (but beta, ~1 maintainer)** | myst-nb stable; theme beta | action (unofficial) | **Med–High** |
| **Sphinx + nbsphinx 0.9.8** | Yes | `nbsphinx_execute="never"` | Medium (MyST for `.md`) + **Pandoc build dep** | via any Sphinx theme (incl. sphinx-immaterial) | Actively maintained | action (unofficial) | **Med–High** |
| **Jupyter Book v1** (Sphinx) | Yes | `execute_notebooks:"off"` | Medium (MyST) | sphinx-book-theme (not Material) | **Maintenance-only — dead end** | Sphinx publish | Med–High — **avoid** |

**Cross-cutting friction if we leave MkDocs.** Every non-MkDocs option shares the
same two real costs — the notebooks themselves are the *easy* part:
- **Markdown dialect.** We use python-markdown + Material admonitions
  (`!!! note`), `attr_list` (`{: .class}`), and `pymdownx` tabs. Quarto wants
  Pandoc (`::: {.callout-note}`), and the MyST-based tools want `:::{note}`.
  Our **27 Markdown files that embed custom `div` grid/button classes** and the 3
  custom CSS files are the fiddly bit to re-home.
- **Theme rebuild.** Only `sphinx-immaterial` reproduces the Material look; every
  other option is a clean-but-different theme, so the visual identity is
  re-created, not inherited.
- **Notebook download button.** Our `page.nb_url` override is replaced by each
  tool's own mechanism — Quarto `notebook-view`/`notebook-links` (nicest),
  nbsphinx source links, or a theme-provided button in Sphinx/JupyterBook.

**Ranked recommendation** (weighing: notebooks with minimal rework · Material-like
look + search · active maintenance · easy GitHub Pages):

1. **Stay on MkDocs 1.x + Material + mkdocs-jupyter — for now.** Uniquely wins on
   rework (zero), look (already Material), and deploy (unchanged); the plugin is
   actively maintained. Only weakness is the frozen core/theme. **Pin all
   versions, keep 3.9–3.12, keep shipping, and re-check in 6–12 months** —
   especially whether Zensical gains a notebook path via its planned third-party
   module system (early-2026 proposal ZAP-007), which would become the
   lowest-friction forward route.
2. **Quarto — best target if/when we move.** Best-maintained (Posit), notebooks
   render un-executed *by default* with native download/view links (retires our
   custom override), official GH Pages Action. Cost: non-Material theme +
   admonition/tab rewrite.
3. **Sphinx + myst-nb + sphinx-immaterial — pick only if a Material look is
   non-negotiable.** The one route that reproduces the Material appearance, but
   the theme is pre-1.0 / effectively single-maintainer, and we'd adopt Sphinx's
   `toctree`/`conf.py` model.
4. **Jupyter Book v2 / mystmd — promising, philosophically closest, still
   stabilizing.** Pilot before committing.
5. **Sphinx + nbsphinx — mature but more moving parts** (Pandoc dep + myst-parser
   for our 101 `.md` pages). **Avoid Jupyter Book v1** (dead end).

**Bottom line:** the notebook blocker doesn't force a bad migration — it argues
for *not* migrating yet. Stay on MkDocs 1.x with pinned versions; when we do move,
the finalists are **Quarto** (best maintenance + notebook story) vs **Sphinx +
myst-nb + sphinx-immaterial** (best Material look, weaker maintenance). Either
way, do a **5–6 notebook + a-few-Markdown-page pilot** — including the custom
grid/button `div`s and the download button — before converting all 148 pages; the
admonition/attr rewrite and theme rebuild are the real cost, not the notebooks.

*Dates flagged as reported/approximate: Material's ~Nov 2026 EOL and Jupyter Book
v2's exact GA status are directional, not hard deadlines.*

---

## Sources
- MkDocs 2.0 / why Zensical: https://squidfunk.github.io/mkdocs-material/blog/2026/02/18/mkdocs-2.0/ , https://squidfunk.github.io/mkdocs-material/blog/2025/11/05/zensical/
- Zensical MkDocs compatibility & migration: https://zensical.org/docs/compatibility/mkdocs/ , https://zensical.org/docs/compatibility/mkdocs/migration/
- Supported plugins: https://zensical.org/docs/compatibility/mkdocs/plugins/
- mkdocs-jupyter status: https://github.com/zensical/zensical/issues/52 , https://github.com/zensical/backlog/issues/9
- Customization / overrides (MiniJinja): https://zensical.org/docs/customization/
- Extensions: https://zensical.org/docs/setup/extensions/about/
- PyPI (version, Python ≥ 3.10): https://pypi.org/project/zensical/

### §6 alternatives
- mkdocs-jupyter (actively maintained): https://pypi.org/project/mkdocs-jupyter/
- Quarto: https://quarto.org/docs/projects/code-execution.html · https://quarto.org/docs/authoring/notebook-embed.html · https://quarto.org/docs/publishing/github-pages.html · https://github.com/quarto-dev/quarto-actions · https://opensource.posit.co/blog/2026-04-06_whats-next-quarto-2/
- Jupyter Book / MyST: https://jupyterbook.org/stable/resources/faq/ · https://mystmd.org/guide/execute-notebooks · https://mystmd.org/guide/deployment-github-pages · https://github.com/jupyter-book/mystmd/releases
- Sphinx + myst-nb: https://myst-nb.readthedocs.io/en/stable/computation/execute.html · https://sphinx-immaterial.readthedocs.io/ · https://pydata-sphinx-theme.readthedocs.io/
- Sphinx + nbsphinx: https://nbsphinx.readthedocs.io/en/latest/never-execute.html · https://github.com/spatialaudio/nbsphinx/releases
