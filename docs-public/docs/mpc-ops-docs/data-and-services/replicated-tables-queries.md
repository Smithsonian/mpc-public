# Replicated PostgreSQL Tables: Sample Queries

This page collects sample SQL queries for the [replicated tables](replicated-tables-schema.md). They are grouped by topic:

- [Conventions and performance notes](#conventions-and-performance-notes)
- [Running the queries from Python](#running-the-queries-from-python)
- [Identifications and designations](#identifications-and-designations)
- [Observations](#observations-obs_sbn)
- [Orbits](#orbits-mpc_orbits)
- [Observatory codes](#observatory-codes-obscodes)
- [Objects on the NEOCP](#objects-on-the-neocp)
- [Alterations and the Isolated Tracklet File (ITF)](#alterations-and-the-isolated-tracklet-file-itf)
- [Aggregate and analytical queries](#aggregate-and-analytical-queries)

The queries are illustrative: except where an example explicitly shows output, we describe the columns a query returns rather than reproducing full result sets (which change as the database is updated).

## Conventions and performance notes

A few conventions recur throughout the replicated schema and are worth understanding before writing your own queries.

**Designations are stored in both packed and unpacked form.** Most identification tables carry, side by side, a *packed* and an *unpacked* column for both the *primary* and any *secondary* provisional designations — for example `packed_primary_provisional_designation` / `unpacked_primary_provisional_designation`. In the observations table the same duality appears as `provid` / `provid_pkd` and `permid` / `permid_pkd`. See the [provisional designation definition](../designations/provisional-designations.md) for the packing rules.

**`permid` vs `provid`.** In `obs_sbn`, `permid` is the IAU permanent designation (the number, for a numbered minor planet) and is empty for un-numbered objects; `provid` is the unpacked MPC-assigned provisional designation. To go from a provisional designation to a number, join through the identification tables (see the examples below).

**Observation-status values.** The `obs_sbn.status` column takes one of three values:

| `status` | Meaning |
|----------|---------|
| `P` | Officially published in a circular (DOU, mid-month, or monthly). |
| `p` | Accepted and waiting for publication in the next circular. |
| `I` | Isolated Tracklet File (ITF) observation. |

Observations marked `deprecated = 'X'` are preserved for historical purposes and **must not** be used for orbit fitting; filter them out unless you specifically want them.

!!! warning "Bound your `obs_sbn` queries"
    `obs_sbn` is by far the largest table. Always constrain it by `status` and/or an `obstime` date range, and make sure the relevant [indexes](replicated-tables-intro.md#indexes) exist — an unbounded scan of the whole table can be very slow. Note that `obstime` is stored as text; the examples cast it with `obstime::date` for date-range comparisons.

## Running the queries from Python

The queries on this page are plain SQL and can be run from any PostgreSQL client — `psql`, a GUI such as DBeaver, or a program. Because the database is one you [replicate locally from the SBN](replicated-tables-intro.md), the connection details (host, database name, user, password) are your own: the MPC does not host a public SQL endpoint.

A minimal connection and query with [`psycopg`](https://www.psycopg.org/):

```python
import psycopg  # psycopg 3: pip install "psycopg[binary]"  (for psycopg2: import psycopg2 as psycopg)

conn = psycopg.connect(host="localhost", dbname="mpc_sbn", user="mpc_read", password="********")

with conn.cursor() as cur:
    cur.execute(
        "SELECT unpacked_secondary_provisional_designation "
        "FROM current_identifications "
        "WHERE unpacked_primary_provisional_designation = %s;",
        ("2015 AC2",),
    )
    for row in cur.fetchall():
        print(row)
```

!!! warning
    Always pass values as query **parameters** (the `%s` placeholder and the tuple above), never by string-formatting them into the SQL. This avoids SQL-injection problems and quoting mistakes with designations that contain spaces.

For interactive analysis it is often convenient to read results straight into a [pandas](https://pandas.pydata.org/) DataFrame through a [SQLAlchemy](https://www.sqlalchemy.org/) engine:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://mpc_read:********@localhost/mpc_sbn")

df = pd.read_sql(
    """
    SELECT unpacked_primary_provisional_designation, a, e, i, h
    FROM mpc_orbits
    WHERE orbit_type_int = 2       -- Apollo
    LIMIT 1000;
    """,
    engine,
)
print(df.describe())
```

!!! tip
    A runnable, end-to-end version of these examples is available as a Jupyter notebook: [Querying the replicated database](../../tutorials/notebooks/mpc_tutorial_replicated_db_queries.ipynb). It requires access to your own replicated database.

## Identifications and designations

### To retrieve all the secondary designations for a given primary designation

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

### To retrieve all the secondary designations for a generic designation

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

### To check if an object is numbered

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

### To retrieve the permid for a given object

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

### To retrieve the number, name and naming citation for an object

The `numbered_identifications` table carries the IAU number (`permid`), the IAU name (`iau_name`) and the naming credit; the full naming citation and the discoverers are held in `minor_planet_names`:

```sql
SELECT ni.permid, ni.iau_name, ni.naming_credit,
       mpn.citation, mpn.discoverers
FROM numbered_identifications ni
LEFT JOIN minor_planet_names mpn
  ON ni.permid = mpn.mp_number
WHERE ni.unpacked_primary_provisional_designation = '2015 AC2';
```

!!! note
    Comet names are held separately, in the `comet_names` table.

## Observations (`obs_sbn`)

The `obs_sbn` table holds every published observation plus the Isolated Tracklet File (ITF). Remember the [performance note](#conventions-and-performance-notes): always bound these queries by `status` and/or an `obstime` date range.

### To retrieve all the observations for a numbered object

The following query returns all the MPC-1992 80-column format for the numbered object *123456*:

```sql
SELECT obs80
FROM obs_sbn
WHERE permid = '123456';
```

!!! note
    If an object is numbered, the *permid* field is populated with the same unpacked number.

[Back to introduction](replicated-tables-intro.md)

### To retrieve all the observations for an unnumbered object

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

### To retrieve observations from a particular observatory over a date range

```sql
SELECT obs80_bit, stn, obstime,
       COALESCE(permid_pkd, provid_pkd, trksub) AS designation
FROM obs_sbn
WHERE stn = '703'
  AND status IN ('P', 'p')
  AND obstime::date BETWEEN '2024-01-01' AND '2024-01-31'
ORDER BY obstime;
```

`COALESCE(permid_pkd, provid_pkd, trksub)` is the standard way to pick the best available identifier for each row: the packed number if the object is numbered, otherwise the packed provisional designation, otherwise the observer's tracklet sub-identifier.

!!! warning
    Always keep the `status` and date-range filters on `obs_sbn`: a query over all stations and all time can scan the entire table.

### To retrieve only published (or only ITF) observations

```sql
SELECT obs80
FROM obs_sbn
WHERE provid = '2010 HL23'
  AND status = 'P';
```

Change `status` to `'I'` to retrieve only ITF observations, or `'p'` for observations that have been accepted but not yet published. See the [status values](#conventions-and-performance-notes).

## Orbits (`mpc_orbits`)

The `mpc_orbits` table contains a fitted orbit for every designated object for which an orbit could be computed. Each row carries the orbital elements both as individual columns (`a`, `e`, `i`, `q`, `node`, `argperi`, … each with a matching `*_unc` 1-sigma uncertainty) and as a complete [MPC-ORB JSON](../orbits/mpc-orb-json.md) document in the `mpc_orb_jsonb` column. The table is keyed on the *primary* provisional designation.

### To retrieve the orbital elements for an object

```sql
SELECT unpacked_primary_provisional_designation, permid,
       epoch_mjd, a, e, i, q, node, argperi, mean_anomaly,
       h, u_param, earth_moid, is_pha, orbit_type_int
FROM mpc_orbits
WHERE unpacked_primary_provisional_designation = '2015 AC2';
```

Elements are in au and degrees; `epoch_mjd` is the orbit epoch (TT, MJD), `u_param` is the [uncertainty parameter](../orbits/uncertainty-parameter.md), and `earth_moid` is the Earth Minimum Orbit Intersection Distance (au).

!!! tip
    To retrieve orbits for several objects at once, use `IN`:
    ```sql
    SELECT unpacked_primary_provisional_designation, a, e, i, h
    FROM mpc_orbits
    WHERE unpacked_primary_provisional_designation IN ('2015 AC2', '1994 PC1', '2004 MN4');
    ```

### To retrieve the full MPC-ORB JSON for an object

```sql
SELECT mpc_orb_jsonb
FROM mpc_orbits
WHERE unpacked_primary_provisional_designation = '2015 AC2';
```

`mpc_orb_jsonb` is a `jsonb` document; individual fields can be extracted with the PostgreSQL JSON operators (`->`, `->>`, `#>`), or the whole document can be parsed with the [`mpc_orb` Python package](../orbits/mpc-orb-json.md).

### To list objects of a given dynamical type

`orbit_type_int` classifies each orbit (Aten, Apollo, TNO, …); the integer-to-class mapping is documented on the [Orbit Type Definition](../orbits/orbit-types.md) page.

```sql
SELECT unpacked_primary_provisional_designation, a, e, i, h
FROM mpc_orbits
WHERE orbit_type_int = 2          -- Apollo; see the Orbit Type Definition page
ORDER BY unpacked_primary_provisional_designation
LIMIT 100 OFFSET 0;
```

`LIMIT` / `OFFSET` give simple pagination for large result sets.

### To retrieve the orbit for an object given one of its observations

Because the orbit table is keyed on the primary provisional designation, joining it to `obs_sbn` uses the observation's `provid`:

```sql
SELECT o.obs80, orb.a, orb.e, orb.i, orb.h
FROM obs_sbn AS o
JOIN mpc_orbits AS orb
  ON o.provid = orb.unpacked_primary_provisional_designation
WHERE o.provid = '2015 AC2'
  AND o.status IN ('P', 'p');
```

## Observatory codes (`obscodes`)

### To look up an observatory code

```sql
SELECT obscode, name, name_utf8, longitude, latitude,
       rhocosphi, rhosinphi, observations_type
FROM obscodes
WHERE obscode = '703';
```

`longitude` is the east longitude in degrees; `rhocosphi` and `rhosinphi` are the geocentric parallax constants. Omit the `WHERE` clause to list every observatory code.

### To find observatories near a location

```sql
WITH d AS (
    SELECT obscode, name, latitude, longitude,
           sqrt((latitude - 20.71)^2 + (longitude - 203.74)^2) AS dist
    FROM obscodes
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
)
SELECT obscode, name, latitude, longitude, dist
FROM d
WHERE dist < 5
ORDER BY dist;
```

!!! note
    Give the target longitude as an east longitude in the range 0–360 (i.e. `longitude % 360`). This uses a simple planar distance in degrees, which is fine as a "nearby" filter but is not an exact great-circle distance.

## Objects on the NEOCP

Objects currently on the [NEO Confirmation Page](https://minorplanetcenter.net/iau/NEO/toconfirm_tabular.html) are described by several tables. In all of them the `desig` column holds the observer-assigned temporary designation (the tracklet sub-identifier, `trksub`) — note that this may have been altered by the MPC if a linkage was made, and it is **not** a permanent designation.

### To list the current NEOCP objects, their elements and variant orbits

```sql
SELECT desig, els, digest2 FROM neocp_els ORDER BY desig;   -- nominal elements
SELECT desig, obs80      FROM neocp_obs ORDER BY desig;      -- observations
SELECT desig, els        FROM neocp_var ORDER BY desig, id;  -- variant orbits
```

`els` is a packed elements string. `neocp_var` holds the variant ("clone") orbits used to express the positional uncertainty of each NEOCP object.

### To check whether a tracklet is currently on the NEOCP

```sql
SELECT count(*) != 0 AS on_neocp
FROM neocp_obs
WHERE desig = 'P21abcd';
```

This returns a single boolean.

### To find discovery observations in the NEOCP archive

`neocp_obs_archive` retains tracklets after they leave the live NEOCP. Column 13 of the 80-column record is `*` for the discovery observation:

```sql
SELECT desig, trkid, substring(obs80, 16, 17) AS epoch
FROM neocp_obs_archive
WHERE substring(obs80, 13, 1) = '*';
```

## Alterations and the Isolated Tracklet File (ITF)

### To retrieve all ITF observations

The Isolated Tracklet File is the set of observations that are not (yet) linked to a designated object; they carry `status = 'I'`:

```sql
SELECT obs80, trkid, trksub
FROM obs_sbn
WHERE status = 'I'
ORDER BY trksub, obs80_bit;
```

!!! warning
    The ITF is large. If you are dumping all of it, increase the session working memory first, e.g. `SET work_mem TO '256MB';`.

### To find observations that were redesignated

The `obs_alterations_*` tables record changes made to already-published observations. For example, observations that were moved from one designation to another:

```sql
SELECT obsid,
       unpacked_provisional_designation_from,
       unpacked_provisional_designation_to,
       new_designation_created, publication_ref
FROM obs_alterations_redesignations
WHERE new_designation_created = true;
```

Each alteration row keys back to a specific observation via `obsid` (join to `obs_sbn.obsid`). The companion tables share the same shape: `obs_alterations_corrections`, `obs_alterations_deletions`, and `obs_alterations_unassociations` (the last records observations that were moved to the ITF).

## Aggregate and analytical queries

### To count observations per object

```sql
SELECT provid, count(*) AS n_obs,
       min(obstime) AS first_obs, max(obstime) AS last_obs
FROM obs_sbn
WHERE provid = '2015 AC2'
  AND status IN ('P', 'p')
GROUP BY provid;
```

### To count observations submitted by each observatory in a period

```sql
SELECT stn, count(*) AS n_obs
FROM obs_sbn
WHERE status IN ('P', 'p')
  AND obstime::date BETWEEN '2024-01-01' AND '2024-01-31'
GROUP BY stn
ORDER BY n_obs DESC;
```

!!! warning
    Aggregations over `obs_sbn` still scan every row matching the `WHERE` clause — keep the date/status filters tight and make sure the supporting [indexes](replicated-tables-intro.md#indexes) exist.

[Back to introduction](replicated-tables-intro.md)
