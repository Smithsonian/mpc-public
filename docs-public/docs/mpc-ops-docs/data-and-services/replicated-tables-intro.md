# Replicated PostgreSQL Tables: Introduction and Examples

The MPC makes its PostgreSQL database of observations and orbits available for replication via the [SBN](https://sbnmpc.astro.umd.edu/MPC_database/statusDB.shtml). The schema for the replicated tables is available [here](replicated-tables-schema.md).

## Schema

A description of the database schema is available [here](replicated-tables-schema.md).

## Indexes

[Indexes](https://www.postgresql.org/docs/current/indexes.html) are a powerful tool to boost database performance by enabling faster retrieval of specific rows. However, they come with added overhead, so it's important to use them sensibly.

For users replicating the database from SBN, each index added to the database impacts write time. While this effect is minimal for smaller tables, it can be significant for larger ones, such as the observations table. In extreme cases, excessive indexing can cause the user's database to lag behind the publication database, potentially leading to replication issues. Therefore, users should implement only the essential indexes necessary for their queries.

It's important to note that subscribers have full control over the indexes in their database: neither the MPC nor the SBN manage these. Upon initiating replication from the SBN, subscribers receive two scripts: one to establish the basic subscription and another to add various optional indexes. We recommend that users add only the indexes needed for their specific queries, though they're free to implement additional indexes as desired to support their operations.

### Examples

To create an index on the *updated_at* column of the *observations* table, please run the following command:

```sql
CREATE INDEX obs_updated_at_idx ON public.obs_sbn USING btree (updated_at);
```

For more details on the syntax and options available for creating indexes, please refer to the [PostgreSQL documentation](https://neon.tech/postgresql/postgresql-indexes/postgresql-create-index/).

## Sanity Checks

Subscribers should regularly verify that their replicated database is performing optimally and staying current with the data from the MPC via SBN. There are various ways to do this, but the following straightforward approach may be helpful:

- **Ensure the Observations Table is Up-to-Date**

    Subscribers can view the number of observations in the *obs_sbn* table and check the latest update timestamp. This information is accessible under the "Replication status view MPC-master → [SBN] → MPC-replica" section on the [SBN database status page](https://sbnmpc.astro.umd.edu/MPC_database/statusDB.shtml).

- **Comparison of data consistency**

    Subscribers should compare their version of the *obs_sbn* table with these sources to ensure it is close in size and update time (allowing for minor differences due to data transfer times).
    A sample query to check the size and latest update date is:

    ```sql
    SELECT COUNT(*), MAX(updated_at) FROM obs_sbn;
    ```

    The time required to execute this query will depend on the indexed fields.

## Sample Queries

We have collected some [sample queries](replicated-tables-queries.md) that can be run on the replicated tables. Please note that the queries might take a long time to run, especially on the *obs_sbn* table if the proper indexes are not in place.

- [To retrieve all the secondary designations for a given primary designation](replicated-tables-queries.md#to-retrieve-all-the-secondary-designations-for-a-given-primary-designation)
- [To retrieve all the secondary designations for a generic designation](replicated-tables-queries.md#to-retrieve-all-the-secondary-designations-for-a-generic-designation)
- [To check if an object is numbered](replicated-tables-queries.md#to-check-if-an-object-is-numbered)
- [To retrieve the *permid* for a given object](replicated-tables-queries.md#to-retrieve-the-permid-for-a-given-object)
- [To retrieve all the observations for a numbered object](replicated-tables-queries.md#to-retrieve-all-the-observations-for-a-numbered-object)
- [To retrieve all the observations for an unnumbered object](replicated-tables-queries.md#to-retrieve-all-the-observations-for-an-unnumbered-object)

We plan to add additional sample queries to the documentation as new tables, such as the orbit tables, are finalized.
To check the current status for all the replicated tables, please refer to the [schema page](replicated-tables-schema.md).
