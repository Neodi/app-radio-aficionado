from typing import Optional, List, Dict
from pydantic import BaseModel
from datetime import datetime

from src.domain.quiz.quiz_question_model import QuizQuestionModel


class ExamSessionModel(BaseModel):
    id: str
    user_id: Optional[str]
    questions: List[QuizQuestionModel]
    answers: Dict[str, int] # Mapeo de question_id a selected_option_index
    score: Optional[int] = None
    is_completed: bool = False
    created_at: datetime = datetime.now()
    completed_at: Optional[datetime] = None


