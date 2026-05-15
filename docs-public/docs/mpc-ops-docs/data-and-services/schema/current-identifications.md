# Schema: current_identifications

The current identifications table contains primary objects (minor planets, comets, and natural satellites) and their secondary designations, along with related metadata. The table is continuously updated when a new object is designated or a new identification is created.

## Useful information

- Both packed and unpacked forms are included for primary and secondary designations.
- Every row represents a single identification of an object.
    - If the object has no secondary designations, the primary and secondary fields are the same and appear once (A=A).
    - If the object has one secondary designation, the primary appears twice: once as A=A and once as A=B, where A is the primary designation and B is the secondary designation.
    - If the object has *n* secondary designations, the primary appears *n+1* times.
- For <em>object_type</em>, see the [object types documentation](../../orbits/object-types.md). This value is synchronized with <em>object_type</em> in the [primary_objects table](primary-objects.md) for the corresponding primary designation.
- Every entry in [primary_objects table](primary-objects.md) must have a corresponding entry in the <em>current_identifications</em> table, and viceversa.
- The designations can be linked to the [numbered identifications table](numbered-identifications.md) by primary designation, using either the packed or unpacked form. Objects that have been numbered have the <em>numbered</em> flag set to <em>True</em>.
- Comet fragments are not included in this table; they are disseminated through a separate table.
- Although the packed primary designation is available, the MPC strongly recommends using unpacked primary designations in queries.
- Objects can disappear from the table only if the primary designation is [retired](https://data.minorplanetcenter.net/explorer/?tab=Lists&list=Retired+Designations).
- Please [contact the MPC](https://mpc-service.atlassian.net/servicedesk/customer/portals) if you experience any issues with this table.

| Column | Data type | Description | Nullable |
|--------|-----------|-------------|----------|
| id | integer | PostgreSQL automatically generated identifier for row of data | Not Null |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| packed_secondary_provisional_designation | text | Packed form of a secondary provisional designation (e.g. K06Sf5M) | Not Null |
| packed_primary_provisional_designation | text | Packed form of the primary provisional designation (e.g. K17P08M) | Not Null |
| unpacked_secondary_provisional_designation | text | Unpacked form of a secondary provisional designation (e.g. 2006 SM415) | Not Null |
| unpacked_primary_provisional_designation | text | Unpacked form of the primary provisional designation (e.g. 2017 PM8) | Not Null |
| numbered | boolean | Flag indicating if the primary designation is also numbered | |
| published | integer | Publication status: 0=not published, 1=MPEC, 2=DOU, 3=mid-month circular, 4=monthly circular | |
| identifier_ids | text[] | List of unique identifiers for tracking credit for correct identifications | Not Null |
| object_type | integer | Object classification based on orbital elements | |
-----

## Useful queries
- Our [Replicated PostgreSQL Tables: Sample Queries][replicated-tables-queries.md] page contains useful queries around the <em>current_identifications</em> table.

[Back to schema overview](../replicated-tables-schema.md)
