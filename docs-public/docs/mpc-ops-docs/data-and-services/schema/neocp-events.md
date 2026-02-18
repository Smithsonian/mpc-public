# Schema: neocp_events

The NEOCP events table contains information about main processing events that change the status of NEOCP objects.

| Column | Data type | Description |
|--------|-----------|-------------|
| event_text | text | Full description of the event (e.g. "Additional obs posted to NEOCP" or "Object designated K23W00001U (MPEC 2023-W67)") |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| event_type | text | Event type (e.g. update, add, remove object) |
| desig | text | Observer-assigned object identifier |
| id | integer | PostgreSQL automatically generated identifier for row of data |
| event_user | text | User or process that handled the event (e.g. process_newneo, dbell) |

[Back to schema overview](../replicated-tables-schema.md)
