"""
Entidades del dominio para el sistema de cuestionarios de radioaficionados.
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from uuid import uuid4, UUID

class Title(BaseModel):
    """Modelo para el título de una pregunta."""
    text: str = Field(..., description="Texto del título de la pregunta")
    image: Optional[str] = Field(None, description="Ruta de la imagen del título, si existe")

class Option(BaseModel):
    """Modelo para una opción de respuesta."""
    text: Optional[str] = Field(None, description="Texto de la opción")
    image: Optional[str] = Field(None, description="Ruta de la imagen de la opción, si existe")
    
    @validator('text', 'image')
    def at_least_one_content(cls, v, values):
        """Asegurar que al menos uno de text o image esté presente."""
        if not v and not values.get('text') and not values.get('image'):
            raise ValueError('Al menos text o image debe estar presente')
        return v

class QuizQuestion(BaseModel):
    """Modelo principal para una pregunta del cuestionario."""
    id: str = Field(default_factory=lambda: str(uuid4()), description="ID único de la pregunta")
    original_id: Optional[str] = Field(None, description="ID original de la pregunta del sitio web")
    title: Title = Field(..., description="Título de la pregunta")
    options: List[Option] = Field(..., min_items=2, description="Lista de opciones de respuesta")
    correct_option: int = Field(..., ge=0, description="Índice de la opción correcta (base 0)")
    is_image_question: bool = Field(False, description="Indica si es una pregunta con opciones de imagen")
    
    @validator('correct_option')
    def correct_option_in_range(cls, v, values):
        """Validar que el índice de la opción correcta esté dentro del rango de opciones."""
        options = values.get('options', [])
        if options and v >= len(options):
            raise ValueError(f'correct_option ({v}) debe ser menor que el número de opciones ({len(options)})')
        return v
    
    class Config:
        """Configuración del modelo."""
        json_encoders = {
            UUID: str
        }
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "original_id": "q_001",
                "title": {
                    "text": "¿Cuál es la frecuencia de la banda de 2 metros?",
                    "image": None
                },
                "options": [
                    {"text": "144-148 MHz", "image": None},
                    {"text": "430-440 MHz", "image": None},
                    {"text": "28-29.7 MHz", "image": None},
                    {"text": "145-146 MHz", "image": None}
                ],
                "correct_option": 0,
                "is_image_question": False
            }
        }
    
    def to_legacy_dict(self) -> dict:
        """Convierte el objeto a un diccionario con el formato legacy para compatibilidad."""
        return {
            "question": self.title.text,
            "answers": [opt.text for opt in self.options],
            "correct_answer": self.options[self.correct_option].text if self.correct_option < len(self.options) else None,
            "correct_index": self.correct_option,
            "image": self.title.image,
            "is_image_question": self.is_image_question,
            "answer_images": [opt.image for opt in self.options] if self.is_image_question else None
        }