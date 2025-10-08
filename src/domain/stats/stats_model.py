"""Modelo de estadísticas del usuario."""

from pydantic import BaseModel


class StatsModel(BaseModel):
    """Modelo de estadísticas del usuario."""

    all_exams: list[str]
    passed_exams: list[str]

    category_scores: dict[str, float]

    total_questions: int
    unique_questions: int

    @property
    def total_exams(self) -> int:
        """Retorna el total de exámenes realizados."""
        return len(self.all_exams)

    @property
    def pass_rate(self) -> float:
        """Calcula la tasa de aprobados como porcentaje."""
        if self.total_exams == 0:
            return 0.0
        return (len(self.passed_exams) / self.total_exams) * 100 * len(self.all_exams)
