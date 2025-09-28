"""
Implementación del repositorio de preguntas usando archivos JSON.
Esta implementación pertenece a la capa de infraestructura.
"""
import json
import os
from typing import List, Optional
from ...domain.entities.quiz_question import QuizQuestion
from ...domain.repositories.quiz_repository import QuizQuestionRepository

class JsonQuizQuestionRepository(QuizQuestionRepository):
    """Implementación del repositorio usando archivos JSON."""
    
    def __init__(self, base_path: str = "preguntas"):
        """
        Inicializa el repositorio.
        
        Args:
            base_path: Ruta base donde guardar los archivos
        """
        self.base_path = base_path
    
    def save_questions(self, questions: List[QuizQuestion], filename: str = None) -> bool:
        """Guarda preguntas en formato Pydantic JSON."""
        try:
            if filename is None:
                filename = os.path.join(self.base_path, "quiz_data.json")
            
            # Crear directorio si no existe
            dir_path = os.path.dirname(filename)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            # Convertir objetos Pydantic a diccionarios serializables
            serializable_data = [question.dict() for question in questions]
            
            # Guardar datos en JSON
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(serializable_data, file, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos guardados en '{filename}'")
            print(f"📊 Total de preguntas guardadas: {len(questions)}")
            return True

        except Exception as e:
            print(f"❌ Error al guardar los datos en JSON: {e}")
            return False
    
    def load_questions(self, filename: str = None) -> List[QuizQuestion]:
        """Carga preguntas desde un archivo JSON."""
        try:
            if filename is None:
                filename = os.path.join(self.base_path, "quiz_data.json")
            
            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            
            # Convertir diccionarios a objetos QuizQuestion
            quiz_questions = [QuizQuestion(**question_data) for question_data in data]
            
            print(f"✅ Datos cargados desde '{filename}'")
            print(f"📊 Total de preguntas cargadas: {len(quiz_questions)}")
            
            return quiz_questions

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {filename}")
            return []
        except Exception as e:
            print(f"❌ Error al cargar los datos desde JSON: {e}")
            return []
    
    def save_questions_legacy_format(self, questions: List[QuizQuestion], filename: str = None) -> bool:
        """Guarda preguntas en formato legacy para compatibilidad."""
        try:
            if filename is None:
                filename = os.path.join(self.base_path, "quiz_data_legacy.json")
            
            # Crear directorio si no existe
            dir_path = os.path.dirname(filename)
            if dir_path:
                os.makedirs(dir_path, exist_ok=True)
            
            # Convertir a formato legacy
            legacy_data = [question.to_legacy_dict() for question in questions]
            
            # Guardar datos en JSON
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(legacy_data, file, indent=2, ensure_ascii=False)
            
            print(f"✅ Datos legacy guardados en '{filename}'")
            print(f"📊 Total de preguntas guardadas: {len(legacy_data)}")
            return True

        except Exception as e:
            print(f"❌ Error al guardar los datos legacy en JSON: {e}")
            return False