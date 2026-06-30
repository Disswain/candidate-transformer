from __future__ import annotations

from src.models.candidate import Experience


class ExperienceMapper:

    @staticmethod
    def from_list(items: list) -> list[Experience]:

        experiences: list[Experience] = []

        for item in items:

            experiences.append(
                Experience(
                    company=item.get("company"),
                    title=item.get("title"),
                    start_date=item.get("start_date"),
                    end_date=item.get("end_date"),
                    description=item.get("description"),
                )
            )

        return experiences