# Near-Duplicate Filtering

After observations have been submitted to the Minor Planet Center and have
cleared initial ingest checks, an early phase of the MPC processing pipeline
checks for “near-duplicates”: observations that are already recorded in the MPC
database, with a small but nonzero tolerance for changes in the specific data
values.

Some near-duplicates are “remeasurements”: intentional resubmissions of data
that have undergone improved processing. Others are unintentional, and may even
be of lower quality than the existing data. The early-processing phase of the
MPC pipeline, which cannot know the intentions of the submitter, aims to
automatically accept near-duplicate observations that are definite improvements
over existing data, and reject all other cases.

!!! note

    The default behavior of the early-processing pipeline can be overly 
    conservative for remeasurements. At the moment, there is no mechanism to 
    explicitly flag data as intentional remeasurements, but such a capability
    is planned. In the meantime, if you wish to submit remeasurements, contact
    the MPC via the [MPC Helpdesk] to coordinate submission.

[MPC Helpdesk]: https://mpc-service.atlassian.net/servicedesk/customer/portals


## Definition of Near-Duplication

Identifying near-duplicates is done on an observation-by-observation basis.

Near-duplicate processing is only done for standard optical observations. Radar
observations are not currently checked for near-duplication.

In early MPC processing, two optical observations are judged to be
near-duplicates if:

- They have the same “main” obscode
- They do not have different values for the ADES `fltr` keyword (this is used
  specifically to enable simultaneous multiband data)
- The timestamps are within 5 seconds of each other
- The sky positions are within the obscode’s listed spatial tolerance (in almost
  all cases, this is 2 arcsec)

The obscode-specific spatial tolerance can be adjusted either higher or lower
than the default, depending on the characteristics of the observatory.

Because the early-stage search for near-duplicates is run on every single
incoming observation, it must be quick to evaluate. An initial list of
near-duplicate candidates is constructed by binning observation sky coordinates
onto an N<sub>side</sub> = 32768 HEALpix grid, which has a characteristic pixel
size of 6.4 arcsec. The primary pixel and its immediate neighbors are searched
for potential near-duplicates. Within that list, the angular distances between
the observations are calculated precisely.


## Tracklet-Level Processing

Once near-duplicate observations have been identified, the early-processing
pipeline analyzes the relevant data at the tracklet level.

To make the processing tractable, the pipeline holds tracklets invariant: they
cannot be split or merged at this stage. Therefore, for each tracklet with
near-duplicates, the pipeline must decide whether to accept the new tracklet and
supersede the tracklet(s) it overlaps, or whether to reject the new tracklet and
keep the database unmodified.

The precise algorithm for the determination cannot easily be described because
it turns out that there are many, many corner cases involved. But the short
summary is that the new tracklet is considered for further processing only if it
overlaps every observation in every tracklet that its constituent observations
near-duplicate. If the new tracklet adds more observations that do not
near-duplicate any existing observations (i.e., it is longer than the old
tracklet), that is OK. If, however, the new tracklet does *not* contain an
observation that is found in a tracklet that it overlaps, it will be rejected.

If a new near-duplicate tracklet clears the overlap test, it will be sent to
orbit-fitting. If it makes the resulting fit worse, as checked through a number
of criteria, it will be rejected. Otherwise, the new tracklet is accepted, and
the overlapped tracklets are marked as near-duplicates of the new data.
