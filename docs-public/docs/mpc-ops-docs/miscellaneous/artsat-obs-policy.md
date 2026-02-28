# MPC Policy on Artificial Satellite Observations

## Disposition and Distribution of Observations on Artificial Satellites

The Minor Planet Center, under the auspices of the International Astronomical Union, is the clearing house for astrometric observations of natural bodies within the solar system. Solar System survey projects, particularly those tasked with detecting and tracking NEOs, in the course of routine operations, also frequently collect observations of artificial satellites on distant, "multi-day" geocentric orbits. The astrometric data on artificial satellites, when recognized as such, will be removed from MPC distributed holdings for natural objects. The observations of artificial satellites originating from participating observatories or their organizations that opt-in that their observations can be made available for space situational awareness purposes will be provided via a controlled distribution method to agencies and institutions recognized internationally for providing information for a space safety purpose.

## Suspected Artificial Objects

The Minor Planet Center (MPC) posts submitted observations to the NEO Confirmation Page when they have a high probability of being an unknown NEO, facilitating followup by the NEO community. The MPC actively removes from the NEOCP those tracklets whose motion can be matched with the two-line element set (TLE) of a known artificial object.

A number of the tracklets submitted to the NEOCP cannot be actively matched to a known artificial object, yet have such high rates of motion and such strongly geocentric orbits that there is a very high probability that such tracklets correspond to artificial objects.

### Flagging Criteria

The submitted tracklet is flagged as potentially being artificial ("S") when the score (geoscore) for the object having a geocentric orbit is greater than 10. If any subsequent follow-up decreases the geoscore such that this criteria is no longer met, the object is automatically unflagged.

Any tracklet flagged as potentially artificial that is subsequently identified with a known satellite (e.g. via match with a TLE) will be immediately removed from the NEOCP.

### Accelerated Removal Timelines

Any tracklet flagged as potentially artificial that remains on the NEOCP will be removed automatically on an accelerated basis. The time for removal depends on the geoscore and the 1-sigma positional uncertainty ('unc', in arcmin). The object will be removed from NEOCP after the following time elapses:

- **1.5 days** (geoscore = 100 and unc > 300)
- **2.5 days** (geoscore < 100 and unc > 300)
- **3.5 days** (unc < 300)

The time elapses are from the last observations processed.

Values for the geoscore and sky-plane uncertainties are currently derived from [JPL Scout](https://cneos.jpl.nasa.gov/scout/).

### Sample Data Files

On May 26th 2021, the MPC implemented the above-described flagging of suspected artificial objects. To demonstrate the format of the data once flagging commenced, the following examples were provided:

- [NEOCP](https://www.minorplanetcenter.net/iau/NEO_dev/toconfirm_tabular.html)
- [neocp.txt](https://www.minorplanetcenter.net/iau/NEO_dev/neocp.txt)
- [neocp.json](https://www.minorplanetcenter.net/Extended_Files/neocp_new.json)

!!! note
    The above examples are static files to illustrate the format and are **not** updated in sync with the NEOCP.
