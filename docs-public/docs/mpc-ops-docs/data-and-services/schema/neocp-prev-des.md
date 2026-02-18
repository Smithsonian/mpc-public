# Schema: neocp_prev_des

The previous NEOCP objects table contains a list of objects previously listed on the NEOCP, their designation if designated, and the reasons for their removal.

| Column | Data type | Description |
|--------|-----------|-------------|
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| digest2 | numeric | Digest2 score |
| pkd_desig | text | Extended packed provisional designation |
| ref | text | MPEC reference |
| desig | text | Observer-assigned object identifier |
| id | integer | PostgreSQL automatically generated identifier for row of data |
| status | text | Reasons for removal |
| iau_desig | text | Unpacked provisional designation (IAU format) |

[Back to schema overview](../replicated-tables-schema.md)
