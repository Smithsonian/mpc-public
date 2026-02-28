"""Action Codes API mixin."""

from .exceptions import MPCValidationError


class ActionCodesMixin:

    def request_action_code(self, label):
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
        if not label:
            raise MPCValidationError("label must be a non-empty string")
        return self._post(
            "/api/action-codes/retrieve",
            json={"label": label},
        )
