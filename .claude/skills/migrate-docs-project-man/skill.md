---
name: migrate-docs-project-man
description: View and update the documentation migration tracker
argument-hint: "[update|add|audit|banners] [options]"
---

# Documentation Migration Project Management

Manage the documentation migration tracker at `MIGRATION_TRACKER.md` in the repository root.

**Arguments:** `$ARGUMENTS`

Parse `$ARGUMENTS` to determine the action. If no arguments are provided, default to **display**.

---

## Action: Display (no args)

1. Read `MIGRATION_TRACKER.md` at the repository root.
2. Display the **Summary** and **By Category** tables to the user.
3. Highlight any notable items:
   - Pages with `redirect-needed` or `deprecation-needed` banners
   - High-priority `to-migrate` pages
   - Any inconsistencies noticed (e.g., summary counts don't match detailed tables)

---

## Action: Update (`update <legacy-path> <field>=<value> [<field>=<value> ...]`)

Update a specific entry in the tracker.

1. Read `MIGRATION_TRACKER.md`.
2. Find the row matching `<legacy-path>` in the detailed tables.
3. Update the specified fields. Valid fields:
   - `migration=<migrated|to-migrate|deprecate|skip>`
   - `location=<path>` (new location in docs-public)
   - `banner=<none|redirect-needed|redirect-added|deprecation-needed|deprecation-added|removed>`
   - `notes=<text>`
4. Recalculate the summary counts (both the Status table and the By Category table).
5. Update the `Last updated` date to today.
6. Write the updated file.
7. Report what changed to the user.

---

## Action: Add (`add <legacy-path> --status=<status> --category=<category> [--notes=<text>]`)

Add a new legacy page entry to the tracker.

1. Read `MIGRATION_TRACKER.md`.
2. Verify the entry doesn't already exist (search for `<legacy-path>`).
3. Add a new row to the appropriate category table:
   - Set Migration to `<status>` (default: `to-migrate`)
   - Set New Location to `-`
   - Set Legacy Banner to `none`
   - Set Notes to `<text>` if provided
4. Recalculate the summary counts.
5. Update the `Last updated` date.
6. Write the updated file.
7. Report the addition to the user.

---

## Action: Audit (`audit`)

Cross-check the tracker against the codebase for inconsistencies.

1. Read `MIGRATION_TRACKER.md`.
2. Search all `.md` files under `docs-public/docs/` for `<!-- TODO: update link when migrated -->` comments.
3. For each TODO comment, extract the legacy URL and check:
   - Is the URL in the tracker? If not, flag it as **missing from tracker**.
   - Is the URL marked as `migrated` in the tracker? If so, flag it as **TODO comment should be removed** (the link should be updated to the new local path).
   - Is the URL marked as `skip`? If so, flag the TODO comment as **incorrect** (skip pages don't get migrated, so the TODO is misleading).
4. Check the "Completed Migrations" section of `CLAUDE.md` against the tracker:
   - Every page listed in CLAUDE.md should have a `migrated` row in the tracker.
   - Every `migrated` row in the tracker should have a corresponding entry in CLAUDE.md.
5. Verify summary counts match the detailed tables:
   - Count rows by status in each category table.
   - Compare against the Summary and By Category tables.
6. Report all findings to the user, organized as:
   - **Inconsistencies found** (things that need fixing)
   - **All clear** (checks that passed)

---

## Action: Banners (`banners`)

Show all pages that need manual banner action on the legacy site.

1. Read `MIGRATION_TRACKER.md`.
2. Collect all rows where Legacy Banner is `redirect-needed` or `deprecation-needed`.
3. Display them grouped by type:

   **Redirect banners needed** (migrated pages):
   List each legacy path with its new location, so the user knows what URL to put in the banner.

   **Deprecation banners needed** (deprecated pages):
   List each legacy path with its notes.

4. Provide a count summary: "X redirect banners and Y deprecation banners need to be added."

---

## Recalculating Summary Counts

When recalculating (used by update, add, and audit actions):

1. Count rows in each category's detailed table by Migration status.
2. Update the **By Category** table with the new counts per category.
3. Sum across categories for the **Summary** table:
   - `Migrated` = total rows with `migrated`
   - `Redirect banner needed` = total rows with `redirect-needed`
   - `Redirect banner added` = total rows with `redirect-added`
   - `Legacy page removed` = total rows with banner `removed`
   - `To migrate` = total rows with `to-migrate`
   - `To deprecate` = total rows with `deprecate`
   - `Skip (service/MPEC/data)` = total rows with `skip`
4. Update the `Last updated` date.
