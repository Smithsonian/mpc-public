# Use of MPC APIs

Tutorials on how to use various of the MPC's APIs are linked below.

<div id="contents-grid"></div>

 - [Designation-Identifier API](notebooks/mpc_tutorial_api_designation_identifier.ipynb)
 - [Submission API](notebooks/mpc_tutorial_api_submission_submission.ipynb)
 - [Submission Status API](notebooks/mpc_tutorial_api_submission_status.ipynb)
 - [Orbits API](notebooks/mpc_tutorial_api_orbits.ipynb)
 - [Observatory Codes API](notebooks/mpc_tutorial_api_obscodes.ipynb)
 - [Observations API](notebooks/mpc_tutorial_api_observations.ipynb)
 - [NEOCP Observations API](notebooks/mpc_tutorial_api_neocp_observations.ipynb)
 - [Check Near-Duplicates (CND) API](notebooks/mpc_tutorial_api_cnd.ipynb)
 - [MPECs API](notebooks/mpc_tutorial_api_mpecs.ipynb)
 - [Action Codes API](notebooks/mpc_tutorial_api_action_codes.ipynb)
 - [WAMO API](notebooks/mpc_tutorial_api_wamo.ipynb)
 - [List API](notebooks/mpc_tutorial_api_lists.ipynb)
 - [Magnitude Band API](notebooks/mpc_tutorial_api_mag_band.ipynb)
 - [Pointings API](notebooks/mpc_tutorial_api_pointings.ipynb)
 - [Negative Observations API](notebooks/mpc_tutorial_api_negative_observations.ipynb)
 - [Observing Target List ("WhatsUp") wrapper](notebooks/mpc_tutorial_api_whatsup.ipynb) — an unofficial Python wrapper for a web form, not a formal API

<!-- Note (2026-09-04, resolves the earlier whatsup TODO): /whatsup is the Observing
     Target List web form, working as intended for browsers; it returns 403 only to
     generic HTTP clients that do not send "Accept: text/html". It is not a REST API.
     The tutorial above wraps the form (CSRF token + POST + HTML-table parsing) as a
     convenience. If a real JSON endpoint is ever added, replace that tutorial with a
     standard API tutorial. -->


