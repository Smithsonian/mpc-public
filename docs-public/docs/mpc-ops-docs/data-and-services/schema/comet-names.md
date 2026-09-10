# Schema: comet_names

The comet names table contains the names, primary designations (both packed and unpacked), and references for all the comets that have been named. The table is up-to-date with the bulletins issued by the Small Body Nomenclature Working Group (WGSBN).

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `packed_primary_provisional_designation` | text | Packed form of the primary provisional designation (e.g. J81E29H ). |
| `unpacked_primary_provisional_designation` | text | Unpacked form of the primary provisional designation (e.g. 1981 EH29). |
| `name` | text | Comet name (UTF-8) |
| `naming_publication_references` | text[] | Publication references to WGSBN or MPC. |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
