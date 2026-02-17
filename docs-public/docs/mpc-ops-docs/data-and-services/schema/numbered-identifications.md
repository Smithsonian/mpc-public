# Schema: numbered_identifications

The numbered identifications table contains all numbered objects (minor planets, comets, natural satellites) with their primary provisional designations. The table is continuously updated.

## Useful information

- Both packed and unpacked forms are included for primary provisional designations.
- Only unpacked number (no parentheses) for permanent designations.
- Can be linked to the current identification table via primary provisional designation.

| Column | Data type | Description |
|--------|-----------|-------------|
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| numbered_publication_references | text[] | References to MPC publication(s) about the numbering |
| packed_primary_provisional_designation | text | Packed primary provisional designation (e.g. J81E29H) |
| id | integer | PostgreSQL automatically generated identifier |
| iau_designation | text | Currently unused |
| iau_name | text | Currently unused (MPC not responsible for naming) |
| named_publication_references | text[] | Currently unused |
| naming_credit | text | Currently unused |
| permid | text | Unpacked permanent designation (number, e.g. "500000") |
| unpacked_primary_provisional_designation | text | Unpacked primary provisional designation (e.g. 1981 EH29) |

[Back to schema overview](../replicated-tables-schema.md)
