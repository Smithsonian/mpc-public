# Schema: neocp_var

The NEOCP variant orbits table contains variant orbits for every object on the NEOCP.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `desig` | character varying(16) | Observer-assigned object identifier, unique within a submission batch. It could have been altered by the MPC if linking has been performed between NEOCP objects. |
| `els` | character varying(255) | Orbital element string for each variant orbit in ele220 format. For more information see https://minorplanetcenter.net/mpcops/documentation/ele220/ |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
