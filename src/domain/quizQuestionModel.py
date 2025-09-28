from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4

class Title(BaseModel):
    titleText: str
    titleImage: Optional[str]

class Option(BaseModel):
    optionText: Optional[str]
    optionImage: Optional[str]

class QuizQuestion(BaseModel):
    id: str
    title: Title
    options: List[Option]
    correct_option: int


    def __init__(self, **data):
            if 'id' not in data or not data['id']:
                data['id'] = str(uuid4())
            super().__init__(**data)