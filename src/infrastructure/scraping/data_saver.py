"""
Módulo para guardar los datos del cuestionario en formato JSON.
"""
import json
import os
from typing import List
from src.domain.quiz.quizQuestionModel import QuizQuestion
from ...infrastructure.scraping.duplicate_detector import DuplicateDetector


# def save_quiz_data_to_json(quiz_data: List[QuizQuestion], filename="data/questions.json") -> bool:
#     """
#     Guarda los datos del cuestionario en un archivo JSON.
    
#     Returns:
#         bool: True si el guardado fue exitoso, False en caso contrario
#     """
#     try:
#         # Crear directorio si no existe
#         os.makedirs(os.path.dirname(filename), exist_ok=True)
        
#         # Convertir objetos Pydantic a diccionarios para JSON
#         quiz_data_dict = []
#         for question in quiz_data:
#             # Usar model_dump() de Pydantic v2 para serializar
#             question_dict = question.model_dump()
#             quiz_data_dict.append(question_dict)
        
#         # Guardar datos en JSON
#         with open(filename, "w", encoding="utf-8") as file:
#             json.dump(quiz_data_dict, file, indent=2, ensure_ascii=False)
        
#         print(f"✅ Datos guardados en '{filename}'")
#         print(f"📊 Total de preguntas guardadas: {len(quiz_data)}")
#         return True

#     except Exception as e:
#         print(f"❌ Error al guardar los datos en JSON: {e}")
#         return False


def save_quiz_data_to_json(quiz_data: List[QuizQuestion], file_path: str = "data/questions.json") -> bool:
    """
    Guarda datos del quiz en JSON con detección de duplicados.
    """
    try:
        print("🔍 Iniciando detección de duplicados...")
        duplicate_detector = DuplicateDetector(data_path=file_path)
        unique_questions = duplicate_detector.filter_duplicates(quiz_data)

        if not unique_questions:
            print("ℹ️ No hay preguntas nuevas para guardar")
            return True
        
        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_data =  json.load(f)

        new_data = [question.model_dump() for question in unique_questions]
        all_data = existing_data + new_data

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Guardadas {len(unique_questions)} preguntas nuevas")
        print(f"📁 Total en archivo: {len(all_data)} preguntas")

        return True
    
    except Exception as e:
        print(f"❌ Error al guardar datos: {e}")
        return False


def print_quiz_summary(quiz_data: List[QuizQuestion]):
    """Imprime un resumen de los datos extraídos."""
    if not quiz_data:
        print("❌ No hay datos que mostrar")
        return
    
    print("\n" + "="*60)
    print("📋 RESUMEN DEL CUESTIONARIO EXTRAÍDO")
    print("="*60)
    
    for i, question in enumerate(quiz_data, 1):
        question_text = question.title.titleText if question.title.titleText else "Sin título"
        print(f"\n{i}. {question_text[:80]}...")
        
        # Determinar si es pregunta con imágenes
        has_images = bool(question.title.titleImage) or any(opt.optionImage for opt in question.options)
        print(f"   Tipo: {'🖼️ Imágenes' if has_images else '📝 Texto'}")
        
        # Mostrar respuesta correcta
        if 0 <= question.correct_option < len(question.options):
            correct_answer = question.options[question.correct_option].optionText
            print(f"   Respuesta correcta: {correct_answer}")
        else:
            print(f"   Respuesta correcta: ⚠️ Índice inválido ({question.correct_option})")
            
        if question.title.titleImage:
            print(f"   Imagen de pregunta: {question.title.titleImage}")
    
    print("="*60)