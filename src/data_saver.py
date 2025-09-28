"""
Módulo para guardar los datos del cuestionario en formato JSON.
"""
import json
import os
from typing import List, Union
from domain.quizQuestionModel import QuizQuestion


def save_quiz_data_to_json(quiz_data: List[QuizQuestion], filename="preguntas/quiz_data.json"):
    """Guarda los datos del cuestionario en un archivo JSON usando modelos Pydantic."""
    try:
        # Crear directorio si no existe y filename tiene directorio
        dir_path = os.path.dirname(filename)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        # Convertir objetos Pydantic a diccionarios serializables
        serializable_data = [question.dict() for question in quiz_data]
        
        # Guardar datos en JSON
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(serializable_data, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos guardados en '{filename}'")
        print(f"📊 Total de preguntas guardadas: {len(quiz_data)}")

    except Exception as e:
        print(f"❌ Error al guardar los datos en JSON: {e}")


def save_quiz_data_legacy_format(quiz_data: List[QuizQuestion], filename="preguntas/quiz_data_legacy.json"):
    """Guarda los datos en formato legacy para compatibilidad con código existente."""
    try:
        # Crear directorio si no existe y filename tiene directorio
        dir_path = os.path.dirname(filename)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        
        # Convertir a formato legacy
        legacy_data = [question.to_legacy_dict() for question in quiz_data]
        
        # Guardar datos en JSON
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(legacy_data, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos legacy guardados en '{filename}'")
        print(f"📊 Total de preguntas guardadas: {len(legacy_data)}")

    except Exception as e:
        print(f"❌ Error al guardar los datos legacy en JSON: {e}")


def load_quiz_data_from_json(filename="preguntas/quiz_data.json") -> List[QuizQuestion]:
    """Carga los datos del cuestionario desde un archivo JSON y los convierte a objetos Pydantic."""
    try:
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


def print_quiz_summary(quiz_data: List[QuizQuestion]):
    """Imprime un resumen de los datos extraídos usando objetos Pydantic."""
    if not quiz_data:
        print("❌ No hay datos que mostrar")
        return
    
    print("\n" + "="*60)
    print("📋 RESUMEN DEL CUESTIONARIO EXTRAÍDO")
    print("="*60)
    
    for i, question in enumerate(quiz_data, 1):
        print(f"\n{i}. {question.title.text[:80]}...")
        print(f"   ID: {question.id}")
        if question.original_id:
            print(f"   ID Original: {question.original_id}")
        print(f"   Tipo: {'🖼️ Imágenes' if question.is_image_question else '📝 Texto'}")
        
        # Mostrar opciones
        for j, option in enumerate(question.options):
            marker = "✅" if j == question.correct_option else "  "
            print(f"   {marker} Opción {j+1}: {option.text[:50]}...")
            if option.image:
                print(f"       Imagen: {option.image}")
        
        if question.title.image:
            print(f"   Imagen de pregunta: {question.title.image}")
    
    print("="*60)