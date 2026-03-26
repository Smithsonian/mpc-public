# Command Line Submissions

The Minor Planet Center accepts observations submitted directly to
a script running on our web server. The advantages of using
this method for submitting observations are that the submitter gets an
instant notification that the batch has been received and there is no
transmission via e-mail, meaning that long lines will not be broken.

Starting on 2017 Oct. 30, we now require connections to be made via HTTPS,
rather than HTTP. The examples below reflect this requirement.

---

## Submitting with cURL

The description below assumes that the submission of the observation batch is
via use of the command-line tool cURL. If your script does not work after
changing `http:` to `https:` (or adding `https://`), then check whether your cURL
version supports SSL: `curl -V` should show "https" under "Protocols" and
"SSL" under "Features". You should also ensure that you are running a fairly
recent version of cURL (it is known that V7.19.7 [released in 2009] works, but
V7.12.1 [released in 2004] does not).

To submit observations from the command line (or via a script), simply
issue one of the following commands:

For MPC1992 formatted measurements:

```bash
curl https://minorplanetcenter.net/submit_obs -F "source=<myobs.txt"
```

For ADES XML formatted measurements:

```bash
curl https://minorplanetcenter.net/submit_xml -F "ack=my ack message" -F "ac2=my@email.adr" -F "obj_type=NEO" -F "source=<myobs.xml"
```

For ADES PSV formatted measurements:

```bash
curl https://minorplanetcenter.net/submit_psv -F "ack=my ack message" -F "ac2=my@email.adr" -F "obj_type=NEO" -F "source=<myobs.psv"
```

Where `myobs.???` is replaced with the local file name of the observation
batch you wish to submit. Be sure to include the `<` -- that is very important!

The submitted batch must contain correctly formatted observations, along
with a valid observational header, just as with an e-mail submission.
Note that cURL submissions of MPC1992 formatted measurements require an `AC2` line to indicate where to
send ACKs and designations.

Within a couple of seconds (depending on network latency and size of
batch), you will get back an informational message indicating that the batch
has been transmitted. This message displays a CurlID that you should report
when querying the status of a batch of observations. You will then
receive via e-mail the normal messages associated with the
submission of observations.

Any problems should be reported to the
[MPC](https://cgi.minorplanetcenter.net/cgi-bin/feedback.cgi?U=/iau/mpc.html&S=Feedback&D=M).


## Using Tools Other Than cURL

If you wish to call the script via tools other than cURL, you are not to use the
script listed above for testing purposes.

If you wish to test your script, use `minorplanetcenter.net/submit_obs_test`
instead of `minorplanetcenter.net/submit_obs`. The format of the call
to the test script is exactly the same as that of the functional script. The
test script runs the same basic checks as the functional script. To test
your script, simply issue the following command:

For MPC1992 formatted measurements:

```bash
curl https://minorplanetcenter.net/submit_obs_test -F "source=<myobs.txt"
```

For ADES XML formatted measurements:

```bash
curl https://minorplanetcenter.net/submit_xml_test -F "ack=my ack message" -F "ac2=my@email.adr" -F "obj_type=NEO" -F "source=<myobs.xml"
```

For ADES PSV formatted measurements:

```bash
curl https://minorplanetcenter.net/submit_psv_test -F "ack=my ack message" -F "ac2=my@email.adr" -F "obj_type=NEO" -F "source=<myobs.psv"
```

Where `myobs.???` is replaced with the local file name of the observation
batch you wish to submit. Be sure to include the `<` -- that is very important!
You will get back a CurlID confirming that the batch was received. The submitted
batch is NOT passed to the processing routines for processing.
