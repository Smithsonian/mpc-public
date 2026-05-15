# Replicated PostgreSQL Tables: Schema

The MPC makes its PostgreSQL database of observations and orbits available for replication via the [SBN](https://sbnmpc.astro.umd.edu/MPC_database/statusDB.shtml). Additional information on the replicated tables, including sample queries, can be found [here](replicated-tables-intro.md).

The table below shows the *name*, the *description* and the *status* for all the tables that are currently replicated to the SBN.

The *status* column indicates the table's current state:

- <span style="color:green">**Ready**</span> means the table is fully populated and serves as the MPC's main data source.
- <span style="color:orange">**Partially populated**</span> indicates that while data is being added, further work or consistency checks are needed before it can be fully utilized.
- <span style="color:red">**Not populated**</span> or <span style="color:red">**Empty**</span> signifies that the table is inactive and not yet suitable as a primary data source.
- <span style="color:red">**To be deprecated**</span> indicates that the MPC is planning to deprecate the table and hence remove them from the replicated batch. All the users will be
notified and given enough time to let the MPC know if they prefer for the table to remain active, in case they use it. 

By clicking on the name of each table, you will get to the page of the schema of the specific table, including the column names, types, and descriptions.

| Table name | Description | Status |
|------------|-------------|--------|
| [primary_objects](schema/primary-objects.md) | Table used to keep a record of all the primary designations for minor planets, comets and natural satellites that have been designated by the MPC. | <span style="color:green">Ready</span> |
| [current_identifications](schema/current-identifications.md) | Table containing all the primary designations (minor planets, comets and natural satellites) and their secondary designations, when available. Note that the table won't contain comet fragments. | <span style="color:green">Ready</span> |
| [numbered_identifications](schema/numbered-identifications.md) | Table containing the number and primary provisional designation for any object (minor planet, comet or natural satellites) that have been numbered. The table won't include comet fragments. | <span style="color:green">Ready</span> |
| [obs_sbn](schema/obs-sbn.md) | Table used to record all the observations published by the MPC. Contains observations published by the MPC and associated with designated objects or observations associated with the Isolated Tracklet File (ITF). | <span style="color:green">Ready</span> |
| [obs_alterations_corrections](schema/obs-alterations-corrections.md) | Table used to record the corrections made to the observations that have been published. | <span style="color:red">To be deprecated</span> |
| [obs_alterations_deletions](schema/obs-alterations-deletions.md) | Table used to record the observations that have been deleted by the MPC. | <span style="color:green">Ready</span> |
| [obs_alterations_redesignations](schema/obs-alterations-redesignations.md) | Table used to record the observations that have been redesignated. | <span style="color:red">To be deprecated</span> |
| [obs_alterations_unassociations](schema/obs-alterations-unassociations.md) | Table used to record the observations that were unassociated from their original designation and relocated to the Isolated Tracklet File (ITF). | <span style="color:red">To be deprecated</span> |
| [mpc_orbits](schema/mpc-orbits.md) | Table containing orbits and related information for any minor planet, comet or natural satellite that has been designated and for which it is possible to fit an orbit with the available observations. |<span style="color:orange"> Partially populated</span> |
| [neocp_els](schema/neocp-els.md) | Table containing the nominal orbital element for each tracklet that is currently on the NEOCP. | <span style="color:green">Ready</span> |
| [neocp_events](schema/neocp-events.md) | Table containing NEOCP related processing events. | <span style="color:green">Ready</span> |
| [neocp_obs](schema/neocp-obs.md) | Table containing observations for objects currently on the NEOCP. | <span style="color:green">Ready</span> |
| [neocp_obs_archive](schema/neocp-obs-archive.md) | Table containing archived NEOCP observations. | <span style="color:green">Ready</span> |
| [neocp_prev_des](schema/neocp-prev-des.md) | Table containing objects that were previously listed on the NEOCP, their designation if designated and the reasons for their removal | <span style="color:green">Ready</span>
| [neocp_var](schema/neocp-var.md) | Table containing variant orbits for every object on the NEOCP. | <span style="color:green">Ready</span> |
| [obscodes](schema/obscodes.md) | Table used to keep a record of all the observatory codes assigned by the MPC. | <span style="color:green">Ready</span> |
| [comet_names](schema/comet-names.md) | Table containing a record of all the names assigned to comets by [WGSBN](https://www.wgsbn-iau.org/). | <span style="color:green">Ready</span> |
| [minor_planet_names](schema/minor-planet-names.md) | Table containing a record of all the names assigned to minor planets by [WGSBN](https://www.wgsbn-iau.org/). | <span style="color:green">Ready</span> |
---

