# Schema: obs_alterations_redesignations

The observations alterations redesignations table records observations that have been redesignated -- tracklets officially published in MPC circulars that have now been assigned a brand new designation.

!!! note
    - Usually published in a monthly circular; recorded in `redesigs.dat` in the meantime.
    - MPC is drastically reducing redesignations; this table may be used less in the future.

| Column | Data type | Description |
|--------|-----------|-------------|
| publication_ref | text[] | References to publications announcing the redesignation |
| new_designation_created | boolean | True=new designation was created; False=tracklets associated to existing object |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| status | integer | Publication status: 0=Unpublished, 1=DOU, 2=Monthly Circular |
| packed_provisional_designation_to | text | New packed provisional designation |
| unpacked_provisional_designation_to | text | New unpacked provisional designation |
| id | integer | PostgreSQL automatically generated identifier |
| packed_provisional_designation_from | text | Previous packed provisional designation |
| unpacked_provisional_designation_from | text | Previous unpacked provisional designation |
| obsid | text | MPC observation ID |

[Back to schema overview](../replicated-tables-schema.md)
