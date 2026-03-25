"""Observation Submission API mixin."""

from __future__ import annotations

import os
from typing import Optional, Union

from pydantic import BaseModel, field_validator

from ._base import SUBMIT_BASE_URL, _MixinBase
from ._requests import _validate

# ---------- Request model ----------


class SubmitRequest(BaseModel):
    ack: str
    ac2: str

    @field_validator("ack", "ac2")
    @classmethod
    def _not_empty(cls, v):
        if not v:
            raise ValueError("must be a non-empty string")
        return v


# ---------- Response model ----------


class SubmissionResponse(BaseModel):
    """Response from an observation submission."""

    status_code: int
    """HTTP status code returned by the MPC submission endpoint."""

    message: str
    """Raw response text (typically contains the Submission ID)."""


class SubmissionMixin(_MixinBase):
    def submit_xml(
        self,
        source: Union[str, bytes],
        *,
        ack: str,
        ac2: str,
        obj_type: Optional[str] = None,
        test: bool = True,
    ) -> SubmissionResponse:
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
        SubmissionResponse
            Response with ``status_code`` and ``message`` attributes.
        """
        return self._submit(
            source,
            ack=ack,
            ac2=ac2,
            obj_type=obj_type,
            test=test,
            fmt="xml",
        )

    def submit_psv(
        self,
        source: Union[str, bytes],
        *,
        ack: str,
        ac2: str,
        obj_type: Optional[str] = None,
        test: bool = True,
    ) -> SubmissionResponse:
        """Submit an ADES PSV file of observations.

        Parameters are identical to :meth:`submit_xml`.
        """
        return self._submit(
            source,
            ack=ack,
            ac2=ac2,
            obj_type=obj_type,
            test=test,
            fmt="psv",
        )

    # ------------------------------------------------------------------

    def _submit(
        self,
        source: Union[str, bytes],
        *,
        ack: str,
        ac2: str,
        obj_type: Optional[str],
        test: bool,
        fmt: str,
    ) -> SubmissionResponse:
        req = _validate(SubmitRequest, ack=ack, ac2=ac2)

        suffix = "_test" if test else ""
        path = f"/submit_{fmt}{suffix}"

        data = {"ack": req.ack, "ac2": req.ac2}
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

        return SubmissionResponse(status_code=resp.status_code, message=resp.text)
