"""Submission Status API mixin."""

from .exceptions import MPCValidationError


class SubmissionStatusMixin:

    def get_submission_status(self, submission_id):
        """Check the acceptance status of an MPC observation submission.

        Parameters
        ----------
        submission_id : str
            Submission ID in the format ``YYYY-MM-DDTHH:MM:SS.mmm_xxxxxxxx``.

        Returns
        -------
        dict
            Status dict with keys ``accepted`` (bool),
            ``pipeline_entry_time`` (str or None),
            and ``fault_events`` (list).
        """
        if not submission_id:
            raise MPCValidationError("submission_id must be a non-empty string")
        return self._get(
            "/api/submission-status",
            json={"submission_id": submission_id},
        )
