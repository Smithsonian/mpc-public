# ADES Data Submission

This page describes the Astrometric Data Exchange Standard (ADES) format for submitting
observations to the MPC, including submission procedures, validation, and available resources.

---

## Astrometry Data Exchange Standard

The Astrometry Data Exchange Standard (ADES) is a new data format for
astrometry, providing many new features over the [MPC1992 80-column format](mpc1992-format.md).
The [official format description](https://github.com/IAU-ADES/ADES-Master/blob/master/ADES_Description.pdf)
is on GitHub. See also the reference material [Tables of ADES Tags and Structures](https://github.com/IAU-ADES/ADES-Master/blob/master/ades_master.pdf).

The ADES describes two representations, XML and PSV. PSV is "Pipe Separated
Values", and is similar to comma separated values (CSV) but uses the pipe
character, `|`, rather than a comma to separate data values of a record.
For example see this [example XML](https://minorplanetcenter.net/iau/info/goodsubmit.xml.txt)
and the equivalent [example PSV](https://minorplanetcenter.net/iau/info/goodsubmit.psv.txt).


## "Valid" ADES and Submissions

The E in ADES is for Exchange, which means the standard allows for general
purpose exchange of data. For the special purpose of submitting new data to
the MPC however, there are restrictions on what the general ADES allows. Data
may be valid ADES but not valid for submission. In the context of XML, the
word "valid" can mean that data *validates* by a particular schema.
We validate submissions by a specific schema, [submit.xsd](https://github.com/IAU-ADES/ADES-Master/blob/master/xsd/submit.xsd).
There is a much larger set of data that may still be valid ADES, but will
not validate by submit.xsd.


## Submission Procedures

### HTTPS

ADES submissions are accepted through our web server. Submission by web
form is at [submit_xml](https://minorplanetcenter.net/submit_xml)
for XML and [submit_psv](https://minorplanetcenter.net/submit_psv)
for PSV. Those forms also give examples of how a program such as [cURL](https://en.wikipedia.org/wiki/CURL) can be used to automate
submission through the web server. If you wish to simply check the validity
of a submission in XML format, go [here](https://minorplanetcenter.net/submit_xml_test);
to check the validity of PSV, go [here](https://minorplanetcenter.net/submit_psv_test).

### W3C Schema Validation

We validate all submissions against the W3C schema [submit.xsd](https://github.com/IAU-ADES/ADES-Master/blob/master/xsd/submit.xsd).
We convert PSV submissions to XML for validation. The schema ensures that
the basic structure and content of the data follows the standard. In addition,
we perform a number of checks on submissions, as we have always done for
submissions in the past.

These conversions, validations, and checks are all done by us. You do not
need to perform any of these steps yourself. We will give error messages
in the case of any problems.

### Enumerated Field Values

A number of ADES fields are specified with lists of [allowable values](https://www.minorplanetcenter.net/iau/info/ADESFieldValues.html).

### Other Restrictions

Submissions must generally still follow all restrictions of the [Guide to Minor
Body Astrometry](../astrometry/index.md) except those specific to the 80-column format.

The [Observational Details](observational-details.md) page has restrictions for specifying observer and measurer names.
While the ADES now lists names individually rather than comma separated, the
restrictions for the format of individual names still apply for ADES data.

### Personally Identifiable Information (PII)

Attention was given to removing PII from ADES data. For example, email
addresses formerly given on the AC2 header line are now transmitted outside
of the ADES data document. A goal is to allow ADES data documents to be
placed directly in public archives without modification. Please support
this goal by keeping PII out of ADES submissions, including free format
fields such as comments and remarks.


## Post-Submission Processing

An interim step, as the MPC migrates to the ADES, will be to convert ADES
data to the 80-column format for internal processes that require it. The
program we use is [xmlto80](https://bitbucket.org/mpcdev/xmlto80),
publicly available on Bitbucket. (Note that this is a step we perform
internally -- you are not expected to run this program for routine
submissions. If you can directly produce ADES or PSV format data, please
submit it in that form.)

After 80-column conversion, a problem with your data may be reported back
to you in 80-column format. While the problem report may show your data
in the 80-column format, your data is nevertheless still preserved in its
original form. Use the 80-column data in the problem report as best you can
to understand why your data is being rejected.


## Additional Resources at the GitHub Repository

The GitHub repository [ADES-Master](https://github.com/IAU-ADES/ADES-Master) contains
numerous additional ADES resources.

As described above under ["Valid" ADES and Submissions](#valid-ades-and-submissions),
the ADES has more general purpose than just data submission to the MPC.
Keep this in mind while reviewing the material in the GitHub repository.
Some material describes features and formats that are not acceptable for
submissions.

Additional sample data files are in the [tests](https://github.com/IAU-ADES/ADES-Master/tree/master/tests)
directory. See [test/xml](https://github.com/IAU-ADES/ADES-Master/tree/master/tests/xml)
and [tests/psv](https://github.com/IAU-ADES/ADES-Master/tree/master/tests/psv/validpsv)
for example.

ADES-Master also contains utilities for conversion between the various
formats. However, *there is no need to convert your data for
submission. Generally you should submit data in a format your astrometry
software emits.* Our format preferences are XML, PSV, and 80-column, in
that order, but also our preference is that you submit the first of these that
meets your needs. Do not run a converter program simply because you think
we prefer a different format.

The README.txt file at ADES-Master is extensive and lists all of the
available conversion programs, test scripts, and documentation.


## Problems

Use the general MPC [feedback form](https://cgi.minorplanetcenter.net/cgi-bin/feedback.cgi)
to report problems with the ADES submission process.
