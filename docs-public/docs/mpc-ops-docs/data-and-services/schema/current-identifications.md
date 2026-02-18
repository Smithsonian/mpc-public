# Schema: current_identifications

The current identification table contains all the primary objects (minor planets, comets and natural satellites) and their secondary designations, plus additional information. The table is continuously updated every time a new object is designated or a new identification is created.

## Useful tips

- Both packed and unpacked forms are included for primary and secondary designations.
- Every row represents a single identification of an object.
    - If the object has no secondary designations, primary and secondary fields are the same (appears once).
    - If the object has one secondary designation, the primary appears twice.
    - If the object has *n* (n>1) secondary designations, primary appears *n+1* times.
- For object_type, see the [object types documentation](https://minorplanetcenter.net/mpcops/documentation/object-types/).
- Can be linked to the numbered identifications table by primary designation. Objects that have been numbered will have `numbered` flag set to True.

| Column | Data type | Description |
|--------|-----------|-------------|
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| numbered | boolean | Flag indicating if the primary designation is also numbered |
| published | integer | Publication status: 0=not published, 1=MPEC, 2=DOU, 3=mid-month circular, 4=monthly circular |
| identifier_ids | text[] | List of unique identifiers for tracking credit for correct identifications |
| object_type | integer | Object classification based on orbital elements |
| packed_secondary_provisional_designation | text | Packed form of a secondary provisional designation (e.g. K06Sf5M) |
| packed_primary_provisional_designation | text | Packed form of the primary provisional designation (e.g. K17P08M) |
| id | integer | PostgreSQL automatically generated identifier for row of data |
| unpacked_secondary_provisional_designation | text | Unpacked form of a secondary provisional designation (e.g. 2006 SM415) |
| unpacked_primary_provisional_designation | text | Unpacked form of the primary provisional designation (e.g. 2017 PM8) |

[Back to schema overview](../replicated-tables-schema.md)
