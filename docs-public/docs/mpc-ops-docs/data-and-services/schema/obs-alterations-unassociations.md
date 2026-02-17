# Schema: obs_alterations_unassociations

The observations alterations unassociations table records observations that were unassociated from their current designations. These observations are generally sent to the ITF (Isolated Tracklet File).

!!! note
    When observations are sent to the ITF, the `status` field in `obs_sbn` changes from `P` to `I`.

| Column | Data type | Description |
|--------|-----------|-------------|
| publication_ref | text[] | References to publications announcing the unassociation |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| trkmpc_to | text | New MPC object identifier used to label observations in the ITF |
| id | integer | PostgreSQL automatically generated identifier |
| packed_provisional_designation_from | text | Previous packed provisional designation |
| unpacked_provisional_designation_from | text | Previous unpacked provisional designation |
| obsid | text | MPC observation ID |

[Back to schema overview](../replicated-tables-schema.md)
