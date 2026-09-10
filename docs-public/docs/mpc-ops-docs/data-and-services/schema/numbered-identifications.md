# Schema: numbered_identifications

The numbered identifications table contains all numbered objects (minor planets, comets, natural satellites) with their primary provisional designations. The table is continuously updated.

## Useful information

- Both packed and unpacked forms are included for primary provisional designations.
- Only unpacked number (no parentheses) for permanent designations.
- Can be linked to the current identification table via primary provisional designation.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `packed_primary_provisional_designation` | text | Packed form of the primary provisional designation (e.g. J81E29H ). |
| `unpacked_primary_provisional_designation` | text | Unpacked form of the primary provisional designation (e.g. 1981 EH29). |
| `permid` | text | Unpacked form of the permanent designation (number without parenthesis, e.g. "500000") |
| `iau_designation` | text | This column is currently unused. |
| `iau_name` | text | This column is currently unused. The MPC is not responsible for naming. |
| `numbered_publication_references` | text[] | List of references to any MPC publication(s) including information on the numbering of the corresponding object (e.g. Monthly circulars, etc) |
| `named_publication_references` | text[] | This column is currently unused. The MPC is not responsible for naming. |
| `naming_credit` | text | This column is currently unused. The MPC is not responsible for naming. |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
