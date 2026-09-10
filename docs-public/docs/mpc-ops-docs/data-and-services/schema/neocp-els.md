# Schema: neocp_els

The NEOCP elements table contains the nominal orbital elements for every tracklet that is currently on the NEOCP.

!!! note
    The `desig` field is usually the observer-assigned identifier unless MPC linking has altered it.

<!-- BEGIN GENERATED SCHEMA TABLE — managed by generate_public_schema_docs.py; do not edit below by hand -->

## Columns

| Column | Data type | Description |
|--------|-----------|-------------|
| `id` | integer | PostgreSQL automatically generated identifier |
| `desig` | character varying(16) | Observer-assigned object identifier, unique within a submission batch. It could have been altered by the MPC if linking has been performed between NEOCP objects. |
| `els` | character varying(255) | Orbital element string in the MPC ele220 format. For more information see https://minorplanetcenter.net/mpcops/documentation/ele220/. |
| `dsc_obs` | character varying(255) | 80 or 160-character observation string of the discovery observation. |
| `digest2` | numeric | Digest2 score. For more information see https://ui.adsabs.harvard.edu/abs/2019PASP..131f4501K/abstract and https://ui.adsabs.harvard.edu/abs/2023PASP..135j4505V/abstract |
| `flag` | character(1) | Flag defining if an object is an artificial satellite. Flag=S means that the object matched the TLEs of an artificial satellite; Flag=s means that the object did not match any known artificial satellite, but it looks like one (e.g. high geocentric score) |
| `prep` | character(1) | Flag=P indicating that the object is being prepared for removal |
| `comet` | character(1) | Flag=C indicating that the object is a comet. If the flag is present, the object can also be found on the PCCP (https://minorplanetcenter.net/iau/NEO/pccp_tabular.html) |
| `created_at` | timestamp without time zone | Date and time of initial row insert |
| `updated_at` | timestamp without time zone | Date and time of latest row update |

<!-- END GENERATED SCHEMA TABLE -->

[Back to schema overview](../replicated-tables-schema.md)
