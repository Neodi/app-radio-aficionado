"""
Módulo para guardar los datos del cuestionario en formato JSON.
"""
import json
import os


def save_quiz_data_to_json(quiz_data, filename="data/questions.json"):
    """Guarda los datos del cuestionario en un archivo JSON."""
    try:
        # Crear directorio si no existe
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Guardar datos en JSON
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(quiz_data, file, indent=2, ensure_ascii=False)
        
        print(f"✅ Datos guardados en '{filename}'")
        print(f"📊 Total de preguntas guardadas: {len(quiz_data)}")


    except Exception as e:
        print(f"❌ Error al guardar los datos en JSON: {e}")


def print_quiz_summary(quiz_data):
    """Imprime un resumen de los datos extraídos."""
    if not quiz_data:
        print("❌ No hay datos que mostrar")
        return
    
    print("\n" + "="*60)
    print("📋 RESUMEN DEL CUESTIONARIO EXTRAÍDO")
    print("="*60)
    
    for i, question in enumerate(quiz_data, 1):
        print(f"\n{i}. {question['question'][:80]}...")
        print(f"   Tipo: {'🖼️ Imágenes' if question.get('is_image_question') else '📝 Texto'}")
        print(f"   Respuesta correcta: {question.get('correct_answer', 'No encontrada')}")
        if question.get('image'):
            print(f"   Imagen de pregunta: {question['image']}")
    
    print("="*60)