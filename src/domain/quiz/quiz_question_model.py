from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from pathlib import Path

import hashlib

# Función para obtener rutas dinámicas basadas en categoría
def get_questions_image_dir(category: str) -> Path:
    """Retorna el directorio de imágenes de preguntas para la categoría dada"""
    return Path("assets") / "images" / "questions" / category

def get_options_image_dir(category: str) -> Path:
    """Retorna el directorio de imágenes de opciones para la categoría dada"""
    return Path("assets") / "images" / "options" / category

class TitleModel(BaseModel):
    titleText: str
    titleImage: Optional[str] = None

    def image_full_path(self, category: str) -> Optional[Path]:
        """Retorna la ruta completa de la imagen basada en la categoría"""
        if not self.titleImage:
            return None
        return get_questions_image_dir(category) / self.titleImage
        
    def image_exists(self, category: str) -> bool:
        """Verifica si la imagen existe para la categoría dada"""
        if not self.titleImage:
            return True
        else:
            return self.image_full_path(category).exists() 

class OptionModel(BaseModel):
    optionText: Optional[str]
    optionImage: Optional[str] = None

    def image_full_path(self, category: str) -> Optional[Path]:
        """Retorna la ruta completa de la imagen basada en la categoría"""
        if not self.optionImage:
            return None
        return get_options_image_dir(category) / self.optionImage
    
    def image_exists(self, category: str) -> bool:
        """Verifica si la imagen existe para la categoría dada"""
        if not self.optionImage:
            return True
        return self.image_full_path(category).exists()

class QuizQuestionModel(BaseModel):
    id: str
    title: TitleModel
    options: List[OptionModel]
    correct_option: int
    category: str  # Nueva propiedad para la categoría/temática

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
             "correct_option" : self.correct_option,
             "category": self.category
        }
        content_str = str(sorted(content.items()))
        return hashlib.md5(content_str.encode()).hexdigest()
    
    @property
    def title_hash(self) -> str:
        return hashlib.md5(self.title.titleText.strip().lower().encode()).hexdigest()
    
    def get_questions_image_dir(self) -> Path:
        """Retorna el directorio de imágenes de preguntas para esta pregunta"""
        return get_questions_image_dir(self.category)
    
    def get_options_image_dir(self) -> Path:
        """Retorna el directorio de imágenes de opciones para esta pregunta"""
        return get_options_image_dir(self.category)