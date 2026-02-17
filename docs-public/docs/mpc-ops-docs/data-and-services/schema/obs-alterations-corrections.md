# Schema: obs_alterations_corrections

The observations alterations corrections table records corrections made to published observations.

!!! warning
    The table is currently empty and the schema may change. Remeasurements are still a work in progress.

| Column | Data type | Description |
|--------|-----------|-------------|
| publication_ref | text[] | References to publications announcing the correction |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| id | integer | PostgreSQL automatically generated identifier |
| obsid_new | text | MPC observation ID of the new corrected observation |
| obsid_old | text | MPC observation ID of the old wrong observation that was replaced |

[Back to schema overview](../replicated-tables-schema.md)
