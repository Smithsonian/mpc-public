# Schema: comet_names

The comet names table contains the names, primary designations (both packed and unpacked), and publication references for named comets. The table is kept up to date with bulletins issued by the [Small Body Nomenclature Working Group (WGSBN)](https://www.wgsbn-iau.org/).

| Column | Data type | Description | Nullable |
|--------|-----------|-------------|----------|
| id | integer | PostgreSQL automatically generated identifier for row of data | Not Null |
| created_at | timestamp(6) without time zone | Date and time of initial row insert | |
| updated_at | timestamp(6) without time zone | Date and time of latest row update | |
| name | text | Comet name (UTF-8) | |
| naming_publication_references | text[] | Publication references to [WGSBN](https://www.wgsbn-iau.org/) or MPC | |
| unpacked_primary_provisional_designation | text | Unpacked form of the primary provisional designation (e.g. C/2019 Y4) | Not Null |
| packed_primary_provisional_designation | text | Packed form of the primary provisional designation (e.g. CK19Y040) | Not Null |
---

[Back to schema overview](../replicated-tables-schema.md)
