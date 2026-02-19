# Submission Format for Identifications

Please read the notes below before submitting your identifications. Also, if you wish to
validate your JSON format before submission, there are many JSON validators online;
follow this external [link](https://jsonformatter.org/) for one of them.

Also, MPC criteria specifying what types of identification submissions are automatically
accepted or rejected by the pipeline can be found on the
[criteria page](acceptance-criteria.md).


## Format Requirements

- A header and links section is compulsory.
- Within the header section, `name` and `email` are compulsory.
    - The name you submit should be the same each time you submit a suggested linkage and
      consistent with how your name appears in Minor Planet Electronic Circulars (MPECs)
      e.g. P. Veres or Veres.
    - Please do not include accented characters.
    - **Please do not include special characters such as `{}` or `[]`, otherwise your
      submission will be rejected.**
- Within each link is an optional orbit section and if present the element field-names
  are compulsory.
- For Designations, these should be in the PACKED form whether for numbered (e.g.
  `s2334`) or unnumbered (e.g. `K19XXYY`) designations.
- For tracklets (ITF or NEOCP), the specification requires each to be specified by a
  list composed of `[trkSub, date/date-time, obs-code]`. The date/date-time can be from
  ANY observation in the tracklet and the allowed date/date-time formats are:
    - `YYYYMMDD` e.g. `20200702`
    - `YYYY MM DD.DDDDDDDD` e.g. `2020 07 29.47653005`
    - `YYYY-MM-DDTHH:MM:SSZ` e.g. `2019-01-03T13:18:37Z`
- For NEOCP linkages please supply the extra JSON field in the NEOCP link with "neocp"
  i.e. `"identification_type": "neocp"`. See below for example in the JSON.
- In the JSON format, the backslash, `\`, is a reserved character. However, a trkSub can
  begin with a backslash. Therefore before submission all backslashes will need to be
  escaped i.e. from `\` to `\\`.


## Example JSON Format

Below is an example of the format required for sending potential identification links to
the MPC.

- **Link_0** is an example of: Designations (plural) and ITF tracklet(s)
- **Link_1** is an example of: ONLY designations (plural)
- **Link_2** is an example of: ITF tracklets only (with NEOCP type)
- **Link_3** is an example of: A (i.e. one) designation and ITF tracklet(s)

```json
{
  "header": {
    "name": "J.Doe",
    "email": "j.doe@email.provider.com",
    "comment": "Here are some identifications that I gone and done."
  },
  "links": {
    "link_0": {
      "designations": [
        "K10TD3E",
        "K15A53T",
        "K16G96F"
      ],
      "trksubs": [
        [
          "P10R1G5",
          "20190828",
          "F51"
        ],
        [
          "P10R1G6",
          "20190827",
          "K16"
        ],
        [
          "P10R1X4",
          "20190829",
          "F52"
        ]
      ],
      "orbit": {
        "arg_pericenter": 51.56776,
        "eccentricity": 0.0785125,
        "epoch": 2458894.5,
        "inclination": 3.33483,
        "lon_asc_node": 298.05892,
        "pericenter_distance": 2.56959638,
        "pericenter_time": 2458148.124892
      }
    },
    "link_1": {
      "designations": [
        "K10TD3E",
        "K15A53T",
        "K16G96F"
      ]
    },
    "link_2": {
      "trksubs": [
        [
          "P10R1G5",
          "20190828",
          "F51"
        ],
        [
          "P10R1G6",
          "20190827",
          "K16"
        ],
        [
          "P10R1X4",
          "20190829",
          "F52"
        ]
      ],
      "identification_type": "neocp",
      "orbit": {
        "arg_pericenter": 51.56776,
        "eccentricity": 0.0785125,
        "epoch": 2458894.5,
        "inclination": 3.33483,
        "lon_asc_node": 298.05892,
        "pericenter_distance": 2.56959638,
        "pericenter_time": 2458148.124892
      }
    },
    "link_3": {
      "designations": [
        "K10TD3E"
      ],
      "trksubs": [
        [
          "P10R1G5",
          "20190828",
          "F51"
        ],
        [
          "P10R1G6",
          "20190827",
          "K16"
        ],
        [
          "P10R1X4",
          "20190829",
          "F52"
        ]
      ]
    }
  }
}
```
