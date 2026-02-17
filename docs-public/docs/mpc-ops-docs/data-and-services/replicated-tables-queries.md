# Replicated PostgreSQL Tables: Sample Queries

## To retrieve all the secondary designations for a given primary designation

The *current_identifications* table contains all the current identifications for the objects in the database.
If an object *A* has been linked to an object *B*, the *current_identifications* table contains two entries: one for *A=A* and another one for *A=B*.
The following query returns all the secondary designations for object *A*, when *A* is the primary designation.

```sql
SELECT unpacked_primary_provisional_designation, unpacked_secondary_provisional_designation
FROM current_identifications
WHERE unpacked_primary_provisional_designation = '2015 AC2';
```

The query should return the following results:

```
unpacked_primary_provisional_designation | unpacked_secondary_provisional_designation
------------------------------------------+--------------------------------------------
2015 AC2                                 | 2015 AC2
2015 AC2                                 | 2010 HL23
```

!!! note
    The *current_identifications* table contains both the *packed* and *unpacked* designations.

!!! note
    The previous query only works well if the primary designation is known. For a more generic query see the following example.

[Back to introduction](replicated-tables-intro.md)

## To retrieve all the secondary designations for a generic designation

If the user doesn't know the primary designation, the query to retrieve all the designations associated to the same object is:

```sql
SELECT unpacked_primary_provisional_designation, unpacked_secondary_provisional_designation
FROM current_identifications
WHERE unpacked_primary_provisional_designation = (
    SELECT unpacked_primary_provisional_designation
    FROM current_identifications
    WHERE unpacked_secondary_provisional_designation = '2010 HL23'
);
```

The query should return exactly the same result as above:

```
unpacked_primary_provisional_designation | unpacked_secondary_provisional_designation
------------------------------------------+--------------------------------------------
2015 AC2                                 | 2015 AC2
2015 AC2                                 | 2010 HL23
```

!!! tip
    To obtain the result in JSON format, the query can be modified as follows:

    ```sql
    SELECT to_json(t) FROM(
        SELECT unpacked_primary_provisional_designation, unpacked_secondary_provisional_designation
        FROM current_identifications
        WHERE unpacked_primary_provisional_designation = (
            SELECT unpacked_primary_provisional_designation
            FROM current_identifications
            WHERE unpacked_secondary_provisional_designation = '2010 HL23'
        )
    ) AS t;
    ```

[Back to introduction](replicated-tables-intro.md)

## To check if an object is numbered

The following query checks whether the object *2010 HL23* is numbered and will return a boolean:

```sql
SELECT numbered
FROM current_identifications
WHERE unpacked_secondary_provisional_designation = '2010 HL23';
```

The query should return the following result:

```
 numbered
----------
 t
```

## To retrieve the permid for a given object

If an object is numbered, and you want to look-up its number (*permid*) based on the *unpacked_secondary_provisional_designation*, then the number (*permid*) can be extracted from the *numbered_identifications* table as follows. Please note that the *numbered_identifications* table can only be queried using the primary provisional designation (packed or unpacked) and the primary provisional designation can be obtained with a *join* query with the *current_identifications* table:

```sql
SELECT permid
FROM numbered_identifications ni
JOIN current_identifications ci
ON ni.unpacked_primary_provisional_designation = ci.unpacked_secondary_provisional_designation
WHERE ci.unpacked_primary_provisional_designation = (
    SELECT unpacked_primary_provisional_designation
    FROM current_identifications
    WHERE unpacked_secondary_provisional_designation = '2010 HL23'
);
```

The query should return the following result:

```
 permid
--------
 535308
```

!!! note
    The *permid* field is populated with the unpacked number.

## To retrieve all the observations for a numbered object

The following query returns all the MPC-1992 80-column format for the numbered object *123456*:

```sql
SELECT obs80
FROM obs_sbn
WHERE permid = '123456';
```

!!! note
    If an object is numbered, the *permid* field is populated with the same unpacked number.

[Back to introduction](replicated-tables-intro.md)

## To retrieve all the observations for an unnumbered object

If the object is unnumbered, it might be the result of a linkage, that means that the previous query on the *current_identifications* table needs to be joined with the *obs_sbn* table to retrieve all the observations.

```sql
SELECT obs80
FROM obs_sbn AS o
JOIN current_identifications AS ci
ON o.provid = ci.unpacked_secondary_provisional_designation
WHERE ci.unpacked_secondary_provisional_designation IN (
    SELECT unpacked_secondary_provisional_designation
    FROM current_identifications
    WHERE unpacked_primary_provisional_designation = (
        SELECT unpacked_primary_provisional_designation
        FROM current_identifications
        WHERE unpacked_secondary_provisional_designation = '2010 HL23'
    )
);
```

[Back to introduction](replicated-tables-intro.md)
