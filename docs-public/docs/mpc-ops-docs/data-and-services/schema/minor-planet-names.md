# Schema: minor_planet_names

The minor planet names table contains the names, unpacked permanent designation (number), references, a list of discoverers in JSON format and citations (when available) for all named minor planets. The table is up-to-date with the bulletins issued by the Small Body Nomenclature Working Group (WGSBN).

| Column | Data type | Description |
|--------|-----------|-------------|
| citation | text | Citation associated with the name (can be null) |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| discoverers | json | List of discoverers in JSON format (can be null) |
| name | text | Minor planet name (UTF-8) |
| id | integer | PostgreSQL automatically generated identifier |
| reference | text | Publication references to WGSBN or MPC |
| mp_number | text | Unpacked permanent designation (e.g. 101955) |

[Back to schema overview](../replicated-tables-schema.md)
