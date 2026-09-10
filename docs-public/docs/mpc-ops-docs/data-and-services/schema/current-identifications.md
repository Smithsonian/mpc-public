# Schema: current_identifications

The current identification table contains all the primary objects (minor planets, comets and natural satellites) and their secondary designations, plus additional information. The table is continuously updated every time a new object is designated or a new identification is created.

## Useful tips

- Both packed and unpacked forms are included for primary and secondary designations.
- Every row represents a single identification of an object.
    - If the object has no secondary designations, primary and secondary fields are the same (appears once).
    - If the object has one secondary designation, the primary appears twice.
    - If the object has *n* (n>1) secondary designations, primary appears *n+1* times.
- For object_type, see the [object types documentation](../../orbits/object-types.md).
- Can be linked to the numbered identifications table by primary designation. Objects that have been numbered will have `numbered` flag set to True.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `packed_primary_provisional_designation` | text | Packed form of the primary provisional designation (e.g. K17P08M). |
| `packed_secondary_provisional_designation` | text | Packed form of one of the secondary provisional designations (e.g. K06Sf5M). |
| `unpacked_primary_provisional_designation` | text | Unpacked form of the primary provisional designation (e.g. 2017 PM8). |
| `unpacked_secondary_provisional_designation` | text | Unpacked form of one of the secondary provisional designations (e.g. 2006 SM415). |
| `published` | integer | Integer describing the publication status of the identification: 0=not published, 1=published in an MPEC, 2=published in the DOU, 3=published in a mid-month circular, 4=published in a monthly circular |
| `identifier_ids` | text[] | List of unique identifiers used by the MPC to track credit for correct identifications |
| `object_type` | integer | Object classification based on its orbital element. For more information please see https://minorplanetcenter.net/mpcops/documentation/object-types/ |
| `numbered` | boolean | Flag indicating if the primary designation is also numbered (True if it numbered, False if it is not numbered) |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
