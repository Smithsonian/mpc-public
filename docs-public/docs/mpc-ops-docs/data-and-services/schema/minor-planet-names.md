# Schema: minor_planet_names

The minor planet names table contains the names, unpacked permanent designation (number), references, a list of discoverers in JSON format and citations (when available) for all named minor planets. The table is up-to-date with the bulletins issued by the Small Body Nomenclature Working Group (WGSBN).

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `mp_number` | text | Unpacked permanent designation (e.g. 101955) |
| `name` | text | Minor planet name (UTF-8) |
| `reference` | text | Publication references to WGSBN or MPC. |
| `citation` | text | Citation associated with the name (the citation field can be null). |
| `discoverers` | json | List of discoverers in JSON format (the discoverers field can be null) |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
