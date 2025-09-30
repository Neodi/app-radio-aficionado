from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from pathlib import Path

import hashlib

# Constantes para las rutas de imágenes
QUESTIONS_IMAGE_DIR = Path("assets") / "images" / "questions"
OPTIONS_IMAGE_DIR = Path("assets") / "images" / "options"

class Title(BaseModel):
    titleText: str
    titleImage: Optional[str] = None

    @property
    def image_full_path(self) -> Optional[Path]:
        if not self.titleImage:
            return None
        return QUESTIONS_IMAGE_DIR / self.titleImage
        
    @property
    def image_exists(self) -> bool:
        if not self.titleImage:
            return True
        else:
            return self.image_full_path.exists() 

class Option(BaseModel):
    optionText: Optional[str]
    optionImage: Optional[str] = None

    @property
    def image_full_path(self) -> Optional[Path]:
        if not self.optionImage:
            return None
        return OPTIONS_IMAGE_DIR / self.optionImage
    
    @property
    def image_exists(self) -> bool:
        if not self.optionImage:
            return True
        return self.image_full_path.exists()

class QuizQuestion(BaseModel):
    id: str
    title: Title
    options: List[Option]
    correct_option: int


    def __init__(self, **data):
            if 'id' not in data or not data['id']:
                data['id'] = str(uuid4())
            super().__init__(**data)

    @property
    def fingerprint(self) -> str:
        """Genera un hash único basado en el contenido de la pregunta"""
        content = {
             "title" : self.title.titleText.strip().lower(),
             "options": [opt.optionText.strip().lower() for opt in self.options if opt.optionText],
             "correct_option" : self.correct_option
        }
        content_str = str(sorted(content.items()))
        return hashlib.md5(content_str.encode()).hexdigest()
    
    @property
    def title_hash(self) -> str:
        return hashlib.md5(self.title.titleText.strip().lower().encode()).hexdigest()