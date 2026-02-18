# Schema: neocp_els

The NEOCP elements table contains the nominal orbital elements for every tracklet that is currently on the NEOCP.

!!! note
    The `desig` field is usually the observer-assigned identifier unless MPC linking has altered it.

| Column | Data type | Description |
|--------|-----------|-------------|
| dsc_obs | character varying(255) | 80 or 160-character discovery observation string |
| created_at | timestamp(6) without time zone | Date and time of initial row insert |
| updated_at | timestamp(6) without time zone | Date and time of latest row update |
| digest2 | numeric | Digest2 score |
| comet | character(1) | Flag=C for comet (also on PCCP) |
| flag | character(1) | S=matches TLE of artificial satellite; s=looks like one but no match |
| prep | character(1) | Flag=P for object being prepared for removal |
| desig | character varying(16) | Observer-assigned object identifier |
| els | character varying(255) | Orbital elements in MPC ele220 format |
| id | integer | PostgreSQL automatically generated identifier for row of data |

[Back to schema overview](../replicated-tables-schema.md)
