"""Action Codes API mixin."""

from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel, field_validator

from ._base import _MixinBase
from ._requests import _validate
from .exceptions import MPCValidationError


# ---------- Request model ----------

class ActionCodeRequest(BaseModel):
    label: str

    @field_validator("label")
    @classmethod
    def _label_not_empty(cls, v):
        if not v:
            raise ValueError("label must be a non-empty string")
        return v


class ActionCodesMixin(_MixinBase):

    def request_action_code(self, label: str) -> Dict[str, Any]:
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
        dict
            API response confirming the request.
        """
        req = _validate(ActionCodeRequest, label=label)
        return self._post(
            "/api/action-codes/retrieve",
            json={"label": req.label},
        )
