---
name: migrate-docs
description: Migrate a page from the MPC legacy documentation site into docs-public
argument-hint: "<legacy-url> [--target section/filename.md]"
---

# Migrate Legacy MPC Documentation Page

Migrate a page from the legacy MPC site (`minorplanetcenter.net`) into the new documentation site (`docs-public/docs/mpc-ops-docs/`).

**Arguments:** `$ARGUMENTS`

Parse `$ARGUMENTS` to extract:
- **legacy-url** (required): The URL of the legacy page to migrate
- **--target** (optional): The target path within `docs-public/docs/mpc-ops-docs/` (e.g., `designations/new-page.md`)

---

## Step 1: Fetch and Analyze the Legacy Page

1. Use WebFetch to retrieve the legacy page content from the provided URL.
2. Extract the main content: title, body text, tables, lists, links, code blocks.
3. Identify the content type (reference docs, policy, procedures, data description).
4. Inventory all links on the page, classifying each as:
   - Internal legacy link (potential migration target)
   - External link (third-party site)
   - Service/API endpoint (never migrated)
   - MPEC link (never migrated)
   - Auto-generated data list (never migrated)

---

## Step 2: Determine Target Location — PAUSE FOR APPROVAL

1. If `--target` was provided, use that path as the starting proposal.
2. Otherwise:
   - Read the existing structure under `docs-public/docs/mpc-ops-docs/` using Glob.
   - Examine the closest section's `index.md` to understand existing organization.
   - Propose the best section and filename for the new page.
3. Check whether similar or overlapping content already exists in the new site (search for key terms with Grep). If overlap is found, propose merging.
4. **Use AskUserQuestion** to present:
   - The proposed target path (e.g., `observations/timing-requirements.md`)
   - A brief summary of the content being migrated
   - Any restructuring needed (new subfolder, index page updates)
   - Whether any overlapping content was found

**Do NOT proceed until the user approves the target location.**

---

## Step 3: Convert Content to Markdown

Convert the legacy HTML content to clean, MkDocs-compatible markdown following these rules:

### Formatting
- Preserve tables, code blocks, lists, and all meaningful formatting.
- Use MkDocs Material admonitions where appropriate:
  - `!!! note` for informational callouts
  - `!!! warning` for important caveats
  - `!!! tip` for helpful suggestions
  - `!!! danger` for critical warnings
- Do NOT add emojis.
- Use ATX-style headers (`#`, `##`, `###`).

### Link Conversion Rules

For every link in the content, apply these rules in order:

1. **Already-migrated pages**: Check the "Completed Migrations" section in `CLAUDE.md` and scan existing files under `docs-public/docs/mpc-ops-docs/`. If the link target has been migrated, convert to a relative link to the local `.md` file.
2. **MPEC pages** (`minorplanetcenter.net/mpec/...`): Keep as absolute URL. Never migrate these.
3. **Service/API endpoints** (submission forms, search tools, dynamic pages): Keep as absolute URL. Never migrate these.
4. **Auto-generated data lists** (e.g., `MPNames.html`, `NumberedMPs.html`): Keep as absolute URL. Never migrate these.
5. **Not-yet-migrated documentation pages**: Keep as absolute legacy URL for now. Add a comment `<!-- TODO: update link when migrated -->` after the link.
6. **External links** (non-MPC sites): Keep as-is.

---

## Step 4: Create the New Markdown File

1. Write the converted markdown to `docs-public/docs/mpc-ops-docs/<section>/<filename>.md`.
2. If the target section folder does not exist:
   - Create the section folder.
   - Create an `index.md` for the section with:
     - A top-level heading matching the section name
     - A brief description
     - A `<div class="contents-grid"></div>` followed by a link list (initially containing just the new page)
3. If the section folder exists but has no `index.md`, create one following the same pattern.

---

## Step 5: Update the Parent Index Page

1. Read the section's `index.md`.
2. Add the new page to the appropriate link list:
   - If there is an existing section heading where the page fits, add a link there.
   - If a new section heading is needed, create one.
3. Follow the contents-grid pattern:
   - Button-style links (locally-hosted pages) go in a list immediately after a `<div class="contents-grid"></div>` div.
   - Text links (external/service pages) go in a plain list without the grid div.
4. Use the format: `- [Page title](filename.md)`

### Example of the contents-grid pattern:
```markdown
## Section Name

<div class="contents-grid"></div>

- [Local page title](local-page.md)
- [Another local page](another-page.md)

- [External service link](https://minorplanetcenter.net/some/service)
```

---

## Step 6: Update Cross-References Across the Site

1. Search all `.md` files under `docs-public/docs/` for links pointing to the legacy URL or close variants (with/without trailing slash, with/without `www.`, HTTP vs HTTPS).
2. For each match found:
   - Replace the legacy URL with a relative path to the new local page.
   - If the link was a plain text link and is now pointing to a local page inside a `contents-grid` list, it is already correct.
   - If unclear whether a text link should become a button link, ask the user.
3. Key files to check:
   - `docs-public/docs/mpc-ops-docs/index.md`
   - `docs-public/docs/mpc-ops-docs/observations.md`
   - `docs-public/docs/mpc-ops-docs/orbits.md`
   - `docs-public/docs/mpc-ops-docs/astrometry.md`
   - `docs-public/docs/mpc-ops-docs/observatory-and-program-codes.md`
   - All section `index.md` files under `mpc-ops-docs/`

---

## Step 7: Update CLAUDE.md Migration Notes

1. Open `CLAUDE.md` at the repository root.
2. Find the `### Completed Migrations` section.
3. Add an entry for the newly migrated page under the appropriate section heading.
4. Follow the existing format:
   ```
   - `section/filename.md` - From `/legacy/path`
   ```
5. If migrating into a new section that doesn't have a heading yet, create one following the pattern:
   ```
   **section-name/** (migrated from `source-page.md`):

   - `section-name/filename.md` - Description - From `/legacy/path`
   ```

---

## Step 8: Verify

1. Run the MkDocs build with strict mode to check for broken links or errors:
   ```bash
   cd docs-public && mkdocs build --strict 2>&1 | head -50
   ```
2. Report to the user:
   - What file was created (full path)
   - What files were updated (index pages, cross-references, CLAUDE.md)
   - Any build warnings or errors
   - Any remaining manual steps (e.g., links left as legacy URLs with TODO comments)
   - Any pages linked from the migrated content that should be migrated next

---

## Step 9: Update Migration Tracker

1. Read `MIGRATION_TRACKER.md` at the repository root.
2. Find or add the row for the legacy page that was just migrated in the appropriate category table.
3. Set:
   - **Migration**: `migrated`
   - **New Location**: the relative path of the new file(s) created (e.g., `observations/obs-format.md`)
   - **Legacy Banner**: `redirect-needed`
   - **Notes**: update with any relevant context (e.g., "Consolidated with X")
4. Recalculate the summary counts at the top of the file:
   - Recount each status across all detailed tables
   - Update both the Summary table and the By Category table
   - Update the `Last updated` date to today
5. Write the updated `MIGRATION_TRACKER.md`.
6. Report to the user that the tracker has been updated and that a redirect banner is needed on the legacy page.

---

## Key Rules Reference

These rules govern all MPC documentation migrations:

| Rule | Details |
|------|---------|
| **Button links** | `<div class="contents-grid"></div>` pattern, for locally-hosted pages only |
| **Text links** | Plain markdown links, for external/dynamic/service pages |
| **Never import** | MPEC pages, service/API endpoints, auto-generated data lists |
| **Subfolder threshold** | Create a subfolder with `index.md` when a topic has 3+ related pages |
| **Content location** | All migrated pages go under `docs-public/docs/mpc-ops-docs/<section>/` |
| **No emojis** | Never add emojis to documentation content |
| **mkdocs-jupyter** | Notebooks use `execute: false`, `include_source: true` |
