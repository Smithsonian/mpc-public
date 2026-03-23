"""Action Codes API mixin."""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from ._base import _MixinBase
from ._requests import _validate


# ---------- Request model ----------

class ActionCodeRequest(BaseModel):
    label: str

    @field_validator("label")
    @classmethod
    def _label_not_empty(cls, v):
        if not v:
            raise ValueError("label must be a non-empty string")
        return v


# ---------- Response model ----------

class ActionCodeResponse(BaseModel):
    """Response from an action code retrieval request."""

    model_config = ConfigDict(extra="allow")

    status: Optional[str] = None
    """Status of the request (e.g. ``"ok"``)."""

    message: Optional[str] = None
    """Human-readable message from the API."""


class ActionCodesMixin(_MixinBase):

    def request_action_code(self, label: str) -> ActionCodeResponse:
        """Request retrieval of an action code for a submission.

        The action code will be **emailed** to the original submitter's
        address — it is *not* returned in the API response.

        Parameters
        ----------
        label : str
            Submission identifier (submission ID, tracklet ID, track ID,
            or submission block ID).

        Returns
        -------
        ActionCodeResponse
            API response confirming the request.
        """
        req = _validate(ActionCodeRequest, label=label)
        result = self._post(
            "/api/action-codes/retrieve",
            json={"label": req.label},
        )
        return ActionCodeResponse(**result)
