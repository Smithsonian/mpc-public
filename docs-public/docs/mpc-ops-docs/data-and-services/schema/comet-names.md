# Schema: comet_names

The comet names table contains the names, primary designations (both packed and unpacked), and references for all the comets that have been named. The table is up-to-date with the bulletins issued by the Small Body Nomenclature Working Group (WGSBN).

| Column | Data type | Description |
|--------|-----------|-------------|
| name | text | Comet name (UTF-8) |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| packed_primary_provisional_designation | text | Packed form of the primary provisional designation (e.g. J81E29H) |
| id | integer | PostgreSQL automatically generated identifier for row of data |
| naming_publication_references | text[] | Publication references to WGSBN or MPC |
| unpacked_primary_provisional_designation | text | Unpacked form of the primary provisional designation (e.g. 1981 EH29) |

[Back to schema overview](../replicated-tables-schema.md)
