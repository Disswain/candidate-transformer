"""
Projection Layer.

Projects the canonical Candidate model into the
final configurable JSON output.

Supports:
- Field projection
- Field renaming
- Missing value handling
- Confidence inclusion
- Provenance inclusion
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from src.interfaces.projector import BaseProjector
from src.models.candidate import Candidate


class CandidateProjector(BaseProjector):
    """
    Projects a Candidate into a configurable dictionary.
    """

    def __init__(
        self,
        config: dict[str, Any],
    ) -> None:

        self.config = config

    # -----------------------------------------------------

    def project(
        self,
        candidate: Candidate,
    ) -> dict[str, Any]:

        result: dict[str, Any] = {}

        candidate_dict = candidate.model_dump()

        fields = self.config.get(
            "fields",
            [],
        )

        projection = self.config.get(
            "projection",
            {},
        )

        # -------------------------------------------------
        # Project configured fields
        # -------------------------------------------------

        for field in fields:

            target = field["path"]

            source = field.get(
                "from",
                target,
            )

            value = self._resolve_path(
                candidate_dict,
                source,
            )

            if value is None:

                missing = projection.get(
                    "on_missing",
                    "null",
                )

                if missing == "omit":
                    continue

                if missing == "error":
                    raise ValueError(
                        f"Missing required field '{source}'."
                    )

                result[target] = None

            else:

                result[target] = value

        # -------------------------------------------------
        # Confidence
        # -------------------------------------------------

        if projection.get(
            "include_confidence",
            True,
        ):

            result["confidence"] = (
                candidate.confidence.model_dump()
                if candidate.confidence
                else {}
            )

        # -------------------------------------------------
        # Provenance
        # -------------------------------------------------

        if projection.get(
            "include_provenance",
            True,
        ):

            result["provenance"] = [
                item.model_dump()
                for item in candidate.provenance
            ]

        return result

    # -----------------------------------------------------

    @staticmethod
    def _resolve_path(
        data: Any,
        path: str,
    ) -> Any:
        """
        Resolve nested paths.

        Examples
        --------
        location.country

        links.github

        confidence.overall
        """

        current = data

        for part in path.split("."):

            if isinstance(
                current,
                BaseModel,
            ):
                current = current.model_dump()

            if isinstance(
                current,
                dict,
            ):

                current = current.get(part)

            else:

                return None

            if current is None:
                return None

        return current