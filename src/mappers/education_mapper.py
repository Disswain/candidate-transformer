from __future__ import annotations

from src.models.candidate import Education


class EducationMapper:

    @staticmethod
    def from_list(items: list) -> list[Education]:

        education: list[Education] = []

        for item in items:

            education.append(
                Education(
                    institution=item.get("institution"),
                    degree=item.get("degree"),
                    field=item.get("field"),
                    start_date=item.get("start_date"),
                    end_date=item.get("end_date"),
                )
            )

        return education