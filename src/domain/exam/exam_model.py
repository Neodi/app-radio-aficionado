"""Modelo de datos para una sesión de examen."""

from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel

from src.domain.quiz.quiz_question_model import QuizQuestionModel


class ExamSessionModel(BaseModel):
    """Modelo de datos para una sesión de examen."""

    id: str
    user_id: Optional[str]
    questions: List[QuizQuestionModel]
    answers: Dict[str, int]  # Mapeo de question_id a selected_option_index
    score: Optional[int] = None
    is_completed: bool = False
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None
