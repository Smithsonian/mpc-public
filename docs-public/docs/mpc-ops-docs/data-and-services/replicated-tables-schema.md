# Replicated PostgreSQL Tables: Schema

The MPC makes its PostgreSQL database of observations and orbits available for replication via the [SBN](https://sbnmpc.astro.umd.edu/MPC_database/statusDB.shtml). Additional information on the replicated tables, including sample queries, can be found [here](replicated-tables-intro.md).

The table below shows the *name*, the *description* and the *status* for all the tables that are currently replicated to the SBN.

The *status* column indicates the table's current state:

- **Ready** means the table is fully populated and serves as the MPC's main data source.
- **Partially populated** indicates that while data is being added, further work or consistency checks are needed before it can be fully utilized.
- **Not populated** signifies that the table is inactive and not yet suitable as a primary data source.

By clicking on the name of each table, you will get to the page of the schema of the specific table, including the column names, types, and descriptions.

| Table name | Description | Status |
|------------|-------------|--------|
| [comet_names](schema/comet-names.md) | Table containing a record of all the names assigned to comets by the WGSBN. | Ready |
| [current_identifications](schema/current-identifications.md) | Table containing all the primary designations (minor planets, comets and natural satellites) and their secondary designations, when available. | Ready |
| [minor_planet_names](schema/minor-planet-names.md) | Table containing a record of all the names assigned to minor planets by the WGSBN. | Ready |
| [mpc_orbits](schema/mpc-orbits.md) | Table containing orbits and related information for any minor planet that has been designated and for which it is possible to fit an orbit with the available observations. | Partially populated |
| [neocp_els](schema/neocp-els.md) | Table containing the nominal orbital element for each tracklet that is currently on the NEOCP. | Ready |
| [neocp_events](schema/neocp-events.md) | Table containing NEOCP related processing events. | Ready |
| [neocp_obs](schema/neocp-obs.md) | Table containing observations for objects currently on the NEOCP. | Ready |
| [neocp_obs_archive](schema/neocp-obs-archive.md) | Table containing archived NEOCP observations. | Ready |
| [neocp_prev_des](schema/neocp-prev-des.md) | Table containing objects that were previously listed on the NEOCP, their designation if designated and the reasons for their removal. | Ready |
| [neocp_var](schema/neocp-var.md) | Table containing variant orbits for every object on the NEOCP. | Ready |
| [numbered_identifications](schema/numbered-identifications.md) | Table containing the number and primary provisional designation for any object that have been numbered. | Ready |
| [obs_alterations_corrections](schema/obs-alterations-corrections.md) | Table used to record the corrections made to the observations that have been published. | Empty |
| [obs_alterations_deletions](schema/obs-alterations-deletions.md) | Table used to record the corrections made to the observations that have been published by the MPC and that have also been deleted. | Partially populated |
| [obs_alterations_redesignations](schema/obs-alterations-redesignations.md) | Table used to record the observations that have been redesignated. | Partially populated |
| [obs_alterations_unassociations](schema/obs-alterations-unassociations.md) | Table used to record the observations that were unassociated from their original designation and relocated to the Isolated Tracklet File (ITF). | Partially populated |
| [obscodes](schema/obscodes.md) | Table used to keep a record of all the observatory codes assigned by the MPC. | Ready |
| [obs_sbn](schema/obs-sbn.md) | Table used to record all the observations published by the MPC. Contains observations associated with designated objects and observations associated with the Isolated Tracklet File (ITF). | Ready |
| [primary_objects](schema/primary-objects.md) | Table used to keep a record of all the primary designations for minor planets, comets and natural satellites that have been designated by the MPC. | Ready |
