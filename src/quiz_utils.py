"""
Utilidades adicionales para trabajar con modelos Pydantic QuizQuestion.
"""
from typing import List, Dict, Optional
from domain.quizQuestionModel import QuizQuestion, Title, Option
from data_saver import load_quiz_data_from_json, save_quiz_data_to_json
import json

def filter_questions_by_type(questions: List[QuizQuestion], is_image_question: bool) -> List[QuizQuestion]:
    """Filtra preguntas por tipo (imagen o texto)."""
    return [q for q in questions if q.is_image_question == is_image_question]

def get_questions_by_difficulty(questions: List[QuizQuestion]) -> Dict[str, List[QuizQuestion]]:
    """
    Clasifica preguntas por dificultad basándose en la longitud del texto.
    Esta es una clasificación básica que puedes mejorar con criterios más específicos.
    """
    easy, medium, hard = [], [], []
    
    for question in questions:
        text_length = len(question.title.text) + sum(len(opt.text or "") for opt in question.options)
        
        if text_length < 200:
            easy.append(question)
        elif text_length < 400:
            medium.append(question)
        else:
            hard.append(question)
    
    return {
        "easy": easy,
        "medium": medium,
        "hard": hard
    }

def search_questions(questions: List[QuizQuestion], search_term: str) -> List[QuizQuestion]:
    """Busca preguntas que contengan el término de búsqueda."""
    search_term = search_term.lower()
    results = []
    
    for question in questions:
        # Buscar en el título
        if search_term in question.title.text.lower():
            results.append(question)
            continue
        
        # Buscar en las opciones
        for option in question.options:
            if option.text and search_term in option.text.lower():
                results.append(question)
                break
    
    return results

def get_question_statistics(questions: List[QuizQuestion]) -> Dict:
    """Obtiene estadísticas básicas sobre las preguntas."""
    if not questions:
        return {}
    
    total_questions = len(questions)
    image_questions = len([q for q in questions if q.is_image_question])
    text_questions = total_questions - image_questions
    
    # Contar opciones por pregunta
    options_counts = [len(q.options) for q in questions]
    avg_options = sum(options_counts) / len(options_counts) if options_counts else 0
    
    # Contar preguntas con imágenes en el título
    title_images = len([q for q in questions if q.title.image])
    
    return {
        "total_questions": total_questions,
        "text_questions": text_questions,
        "image_questions": image_questions,
        "questions_with_title_images": title_images,
        "average_options_per_question": round(avg_options, 2),
        "min_options": min(options_counts) if options_counts else 0,
        "max_options": max(options_counts) if options_counts else 0
    }

def export_to_different_formats(questions: List[QuizQuestion], base_filename: str = "quiz_export"):
    """Exporta las preguntas en diferentes formatos."""
    
    # Formato para aplicaciones de quiz
    quiz_format = []
    for q in questions:
        quiz_item = {
            "question": q.title.text,
            "type": "multiple_choice",
            "options": [opt.text for opt in q.options if opt.text],
            "correct_answer": q.correct_option,
            "image": q.title.image,
            "has_image_options": q.is_image_question
        }
        quiz_format.append(quiz_item)
    
    # Guardar formato quiz
    with open(f"{base_filename}_quiz_format.json", "w", encoding="utf-8") as f:
        json.dump(quiz_format, f, indent=2, ensure_ascii=False)
    
    # Formato CSV (para texto simple)
    csv_lines = ["Question,Option1,Option2,Option3,Option4,CorrectAnswer"]
    for q in questions:
        if not q.is_image_question:  # Solo preguntas de texto para CSV
            options = [opt.text or "" for opt in q.options]
            while len(options) < 4:  # Rellenar hasta 4 opciones
                options.append("")
            
            line = f'"{q.title.text}","{options[0]}","{options[1]}","{options[2]}","{options[3]}",{q.correct_option + 1}'
            csv_lines.append(line)
    
    with open(f"{base_filename}_text_only.csv", "w", encoding="utf-8") as f:
        f.write("\n".join(csv_lines))
    
    print(f"✅ Exportado en formato quiz: {base_filename}_quiz_format.json")
    print(f"✅ Exportado en formato CSV: {base_filename}_text_only.csv")

def validate_quiz_data(questions: List[QuizQuestion]) -> Dict[str, List]:
    """Valida los datos del cuestionario y retorna errores encontrados."""
    errors = []
    warnings = []
    
    for i, question in enumerate(questions):
        # Validar que el índice de respuesta correcta está en rango
        if question.correct_option >= len(question.options):
            errors.append(f"Pregunta {i+1}: Índice de respuesta correcta fuera de rango")
        
        # Validar que hay al menos 2 opciones
        if len(question.options) < 2:
            errors.append(f"Pregunta {i+1}: Debe tener al menos 2 opciones")
        
        # Advertir sobre opciones sin texto en preguntas no de imagen
        if not question.is_image_question:
            for j, option in enumerate(question.options):
                if not option.text or option.text.strip() == "":
                    warnings.append(f"Pregunta {i+1}, Opción {j+1}: Texto vacío en pregunta de texto")
        
        # Advertir sobre preguntas sin título
        if not question.title.text or question.title.text.strip() == "":
            warnings.append(f"Pregunta {i+1}: Título vacío")
    
    return {
        "errors": errors,
        "warnings": warnings,
        "is_valid": len(errors) == 0
    }

# Ejemplo de uso
if __name__ == "__main__":
    # Cargar datos existentes
    questions = load_quiz_data_from_json("preguntas/quiz_data.json")
    
    if questions:
        print("📊 Estadísticas del cuestionario:")
        stats = get_question_statistics(questions)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        print("\n🔍 Validación de datos:")
        validation = validate_quiz_data(questions)
        if validation["is_valid"]:
            print("✅ Todos los datos son válidos")
        else:
            print(f"❌ Se encontraron {len(validation['errors'])} errores:")
            for error in validation["errors"]:
                print(f"  - {error}")
        
        if validation["warnings"]:
            print(f"⚠️ Se encontraron {len(validation['warnings'])} advertencias:")
            for warning in validation["warnings"]:
                print(f"  - {warning}")
        
        # Exportar en diferentes formatos
        export_to_different_formats(questions, "preguntas/quiz_export")
        
        # Ejemplos de filtrado
        text_questions = filter_questions_by_type(questions, False)
        image_questions = filter_questions_by_type(questions, True)
        print(f"\n📝 Preguntas de texto: {len(text_questions)}")
        print(f"🖼️ Preguntas con imágenes: {len(image_questions)}")
        
        # Búsqueda de ejemplo
        frequency_questions = search_questions(questions, "frecuencia")
        print(f"\n🔎 Preguntas sobre 'frecuencia': {len(frequency_questions)}")