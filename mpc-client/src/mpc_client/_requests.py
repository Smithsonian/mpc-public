"""Shared Pydantic infrastructure for request validation and response models.

- DictCompatModel: base class for all typed response models
- _validate(): bridges Pydantic ValidationError → MPCValidationError
- _ObsFormatMixin: shared output_format validation for observations and NEOCP
"""
from __future__ import annotations

from typing import Any, List

from pydantic import BaseModel, field_validator
from pydantic import ValidationError as _PydanticValidationError

from .exceptions import MPCValidationError


class DictCompatModel(BaseModel):
    """Base model that supports dict-style access for backward compatibility.

    In addition to attribute access (``model.field``), instances support:
    - ``model["key"]``
    - ``"key" in model``
    - ``model.get("key", default)``
    """

    def __getitem__(self, key: str) -> Any:
        return self.model_dump()[key]

    def __contains__(self, key: object) -> bool:
        return key in self.model_dump()

    def get(self, key: str, default: Any = None) -> Any:
        return self.model_dump().get(key, default)


def _validate(model_cls, **kwargs):
    """Instantiate a request model, re-raising Pydantic errors as MPCValidationError."""
    try:
        return model_cls(**kwargs)
    except _PydanticValidationError as exc:
        messages = "; ".join(
            f"{'.'.join(str(loc) for loc in e['loc'])}: {e['msg']}"
            for e in exc.errors()
        )
        raise MPCValidationError(messages) from exc


class _ObsFormatMixin(BaseModel):
    """Shared output_format + ades_version validation (Observations and NEOCP)."""

    output_format: List[str] = ["XML"]
    ades_version: str = "2022"

    @field_validator("output_format", mode="before")
    @classmethod
    def _coerce_format_to_list(cls, v):
        if isinstance(v, str):
            return [v]
        return v

    @field_validator("output_format")
    @classmethod
    def _check_formats(cls, v):
        _VALID = {"XML", "ADES_DF", "OBS_DF", "OBS80"}
        for fmt in v:
            if fmt not in _VALID:
                raise ValueError(f"Invalid output_format '{fmt}'. Must be one of {_VALID}")
        return v
