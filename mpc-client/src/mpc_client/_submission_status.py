"""Submission Status API mixin."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator

from ._base import _MixinBase
from ._requests import _validate

# ---------- Request model ----------


class SubmissionStatusRequest(BaseModel):
    submission_id: str

    @field_validator("submission_id")
    @classmethod
    def _id_not_empty(cls, v):
        if not v:
            raise ValueError("submission_id must be a non-empty string")
        return v


# ---------- Response models ----------


class FaultEvent(BaseModel):
    """A single fault event recorded by the MPC observation pipeline."""

    model_config = ConfigDict(extra="allow")

    message: str
    """Human-readable description of the fault."""

    phase: int
    """Pipeline phase in which the fault occurred."""

    failure_code: int
    """Numeric code identifying the failure type."""


class SubmissionStatus(BaseModel):
    """Acceptance status of an MPC observation submission."""

    accepted: bool
    """Whether the submission was accepted into the MPC pipeline."""

    pipeline_entry_time: Optional[str] = None
    """ISO timestamp of pipeline ingestion, or ``None`` if not yet ingested."""

    fault_events: List[FaultEvent] = []
    """List of fault events describing rejection reasons, if any."""


class SubmissionStatusMixin(_MixinBase):
    def get_submission_status(self, submission_id: str) -> SubmissionStatus:
        """Check the acceptance status of an MPC observation submission.

        Parameters
        ----------
        submission_id : str
            Submission ID in the format ``YYYY-MM-DDTHH:MM:SS.mmm_xxxxxxxx``.

        Returns
        -------
        SubmissionStatus
            Status with ``accepted`` (bool),
            ``pipeline_entry_time`` (str or None),
            and ``fault_events`` (list).
        """
        req = _validate(SubmissionStatusRequest, submission_id=submission_id)
        data = self._get(
            "/api/submission-status",
            json={"submission_id": req.submission_id},
        )
        return SubmissionStatus(**data)
