"""Observation Submission API mixin."""

import os

from ._base import SUBMIT_BASE_URL
from .exceptions import MPCValidationError, MPCResponseError


class SubmissionMixin:

    def submit_xml(self, source, *, ack, ac2, obj_type=None, test=True):
        """Submit an ADES XML file of observations.

        Parameters
        ----------
        source : str or bytes
            Path to an XML file **or** the raw XML bytes/string.
        ack : str
            Acknowledgement message (required by the MPC).
        ac2 : str
            Email address for notifications (required).
        obj_type : str or None
            Optional object-type flag (e.g. ``"NEO"``).
        test : bool
            If ``True`` (default), submit to the *test* endpoint.
            Set to ``False`` to submit to production.

        Returns
        -------
        dict
            ``{"status_code": int, "message": str}`` where *message*
            is the raw response text (typically contains the Submission ID).
        """
        return self._submit(
            source, ack=ack, ac2=ac2, obj_type=obj_type,
            test=test, fmt="xml",
        )

    def submit_psv(self, source, *, ack, ac2, obj_type=None, test=True):
        """Submit an ADES PSV file of observations.

        Parameters are identical to :meth:`submit_xml`.
        """
        return self._submit(
            source, ack=ack, ac2=ac2, obj_type=obj_type,
            test=test, fmt="psv",
        )

    # ------------------------------------------------------------------

    def _submit(self, source, *, ack, ac2, obj_type, test, fmt):
        if not ack:
            raise MPCValidationError("ack (acknowledgement) is required")
        if not ac2:
            raise MPCValidationError("ac2 (email address) is required")

        suffix = "_test" if test else ""
        path = f"/submit_{fmt}{suffix}"

        data = {"ack": ack, "ac2": ac2}
        if obj_type is not None:
            data["obj_type"] = obj_type

        # Read file contents if source is a filepath
        if isinstance(source, str) and os.path.isfile(source):
            with open(source, "rb") as fh:
                file_bytes = fh.read()
        elif isinstance(source, str):
            file_bytes = source.encode()
        else:
            file_bytes = source

        resp = self._post_raw(
            path,
            data=data,
            files={"source": file_bytes},
            base_url=SUBMIT_BASE_URL,
        )

        return {"status_code": resp.status_code, "message": resp.text}
