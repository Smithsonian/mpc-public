# Schema: numbered_identifications

The numbered identifications table contains numbered objects (minor planets, comets, and natural satellites) with their primary provisional designations. The table is continuously updated.

## Useful information

- Both packed and unpacked forms are included for primary provisional designations.
- Permanent designations are included as unpacked numbers without parentheses.
- The designations can be linked to the [current identifications table](current-identifications.md) by primary designation, using either the packed or unpacked form. Objects that have been numbered have the <em>numbered</em> flag set to <em>True</em> in the [current identifications table](current-identifications.md).
- Please [contact the MPC](https://mpc-service.atlassian.net/servicedesk/customer/portals) if you experience any issues with this table.

| Column | Data type | Description | Nullable |
|--------|-----------|-------------|----------|
| id | integer | PostgreSQL automatically generated identifier for row of data | Not Null |
| created_at | timestamp(6) without time zone | Date and time of initial row insert | |
| updated_at | timestamp(6) without time zone | Date and time of latest row update | |
| packed_primary_provisional_designation | text | Packed primary provisional designation (e.g. J81E29H) | Not Null |
| unpacked_primary_provisional_designation | text | Unpacked primary provisional designation (e.g. 1981 EH29) | Not Null |
| permid | text | Unpacked permanent designation (number, e.g. "500000") | Not Null |
| iau_designation | text | IAU designation (e.g. (500000), currently not used) | |
| iau_name | text | IAU name (currently not used; names for <em>minor planets</em> and <em>comets</em> are available from the [minor planet names](minor-planet-names.md) and [comet names](comet-names.md) tables) | |
| numbered_publication_references | text[] | References to the MPC publication(s) where the object was numbered | |
| named_publication_references | text[] | References to the publication(s) in which the name was assigned (currently not used) | |
| naming_credit | text | Naming credits (currently not used) | |

## Useful queries
- Our [Replicated PostgreSQL Tables: Sample Queries][replicated-tables-queries.md] page contains useful queries around the <em>numbered_identifications</em> table.

[Back to schema overview](../replicated-tables-schema.md)
