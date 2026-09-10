# Schema: neocp_events

The NEOCP events table contains information about main processing events that change the status of NEOCP objects.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `desig` | text | Observer-assigned object identifier, unique within a submission batch. It could have been altered by the MPC if linking has been performed between NEOCP objects. |
| `event_type` | text | Event type, e.g. update, add, remove object |
| `event_text` | text | A full description of the event type for each object, e.g. Additional obs posted to NEOCP or Object designated K23W00001U (MPEC 2023-W67) |
| `event_user` | text | User name of who/what processed the event, e.g. process_newneo (automated process), dbell (human) |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
