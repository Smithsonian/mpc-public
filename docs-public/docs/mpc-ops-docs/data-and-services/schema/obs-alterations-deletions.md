# Schema: obs_alterations_deletions

The observations alterations deletions table records observations that were published (in an MPEC, DOU, or circular) and subsequently deleted. Once deleted, observations disappear from the `obs_sbn` table.

!!! note
    The table alone cannot reproduce all different deletion files published daily (e.g. `todelete.dat`, `removed_obs.dat`).

| Column | Data type | Description |
|--------|-----------|-------------|
| publication_ref | text[] | References to publications announcing the deletion |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| status | integer | Publication status: 0=Unpublished, 1=Published in DOU, 2=Published in Monthly Circular |
| id | integer | PostgreSQL automatically generated identifier for row of data |
| obsid | text | MPC observation ID of the deleted observation |

[Back to schema overview](../replicated-tables-schema.md)
