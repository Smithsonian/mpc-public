# Schema: neocp_var

The NEOCP variant orbits table contains variant orbits for every object on the NEOCP.

| Column | Data type | Description |
|--------|-----------|-------------|
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| desig | character varying(16) | Observer-assigned object identifier |
| els | character varying(255) | Variant orbit in ele220 format |
| id | integer | PostgreSQL automatically generated identifier for row of data |

[Back to schema overview](../replicated-tables-schema.md)
