"""
Módulo para guardar los datos del cuestionario en formato JSON.
"""

import json
import os
from typing import List

from domain.quiz.quiz_question_model import QuizQuestionModel

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


def save_quiz_data_to_json(
    quiz_data: List[QuizQuestionModel], category: str = None, file_path: str = None
) -> int:
    """
    Guarda datos del quiz en JSON con detección de duplicados.

    Args:
        quiz_data: Lista de preguntas del quiz
        category: Categoría de las preguntas (radioelectricidad, normativa, etc.)
        file_path: Ruta del archivo (opcional, se generará automáticamente si no se proporciona)

    Returns:
        int: Número de preguntas nuevas guardadas (-1 si hay error)
    """
    try:
        # Determinar la categoría y ruta del archivo
        if not category and quiz_data:
            category = quiz_data[0].category

        if not file_path:
            if category:
                file_path = f"data/questions_{category}.json"
            else:
                file_path = "data/questions.json"

        print(f"🔍 Iniciando detección de duplicados para categoría: {category}")
        duplicate_detector = DuplicateDetector(data_path=file_path)
        unique_questions = duplicate_detector.filter_duplicates(quiz_data)

        if not unique_questions:
            print(f"ℹ️ No hay preguntas nuevas para guardar en categoría: {category}")
            return 0

        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                existing_data = json.load(f)

        new_data = [question.model_dump() for question in unique_questions]
        all_data = existing_data + new_data

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Guardadas {len(unique_questions)} preguntas nuevas en: {file_path}")
        print(f"📁 Total en archivo: {len(all_data)} preguntas")

        return len(unique_questions)

    except Exception as e:
        print(f"❌ Error al guardar datos: {e}")
        return -1


def print_quiz_summary(quiz_data: List[QuizQuestionModel]):
    """Imprime un resumen de los datos extraídos."""
    if not quiz_data:
        print("❌ No hay datos que mostrar")
        return

    print("\n" + "=" * 60)
    print("📋 RESUMEN DEL CUESTIONARIO EXTRAÍDO")
    print("=" * 60)

    for i, question in enumerate(quiz_data, 1):
        question_text = (
            question.title.titleText if question.title.titleText else "Sin título"
        )
        print(f"\n{i}. {question_text[:80]}...")

        # Determinar si es pregunta con imágenes
        has_images = bool(question.title.titleImage) or any(
            opt.optionImage for opt in question.options
        )
        print(f"   Tipo: {'🖼️ Imágenes' if has_images else '📝 Texto'}")

        # Mostrar respuesta correcta
        if 0 <= question.correct_option < len(question.options):
            correct_answer = question.options[question.correct_option].optionText
            print(f"   Respuesta correcta: {correct_answer}")
        else:
            print(
                f"   Respuesta correcta: ⚠️ Índice inválido ({question.correct_option})"
            )

        if question.title.titleImage:
            print(f"   Imagen de pregunta: {question.title.titleImage}")

    print("=" * 60)
