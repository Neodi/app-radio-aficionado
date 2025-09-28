"""
Servicios de la capa de aplicación para el dominio de cuestionarios.
Contiene la lógica de negocio que no pertenece directamente a las entidades.
"""
from typing import List, Dict, Optional
from ...domain.entities.quiz_question import QuizQuestion
import json
import os

class QuizService:
    """Servicio para operaciones complejas con cuestionarios."""
    
    def validate_questions(self, questions: List[QuizQuestion]) -> Dict[str, List]:
        """
        Valida los datos del cuestionario y retorna errores encontrados.
        
        Args:
            questions: Lista de preguntas a validar
            
        Returns:
            Dict con errores, advertencias y estado de validación
        """
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
    
    def get_statistics(self, questions: List[QuizQuestion]) -> Dict:
        """
        Obtiene estadísticas básicas sobre las preguntas.
        
        Args:
            questions: Lista de preguntas
            
        Returns:
            Dict con estadísticas del cuestionario
        """
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
    
    def search_questions(self, questions: List[QuizQuestion], search_term: str) -> List[QuizQuestion]:
        """
        Busca preguntas que contengan el término de búsqueda.
        
        Args:
            questions: Lista de preguntas donde buscar
            search_term: Término de búsqueda
            
        Returns:
            Lista de preguntas que coinciden con la búsqueda
        """
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
    
    def filter_by_type(self, questions: List[QuizQuestion], is_image_question: bool) -> List[QuizQuestion]:
        """
        Filtra preguntas por tipo (imagen o texto).
        
        Args:
            questions: Lista de preguntas a filtrar
            is_image_question: True para preguntas con imágenes, False para texto
            
        Returns:
            Lista filtrada de preguntas
        """
        return [q for q in questions if q.is_image_question == is_image_question]
    
    def get_questions_by_difficulty(self, questions: List[QuizQuestion]) -> Dict[str, List[QuizQuestion]]:
        """
        Clasifica preguntas por dificultad basándose en la longitud del texto.
        
        Args:
            questions: Lista de preguntas a clasificar
            
        Returns:
            Dict con preguntas clasificadas por dificultad
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
    
    def export_questions(self, questions: List[QuizQuestion], format_type: str, base_filename: str = "quiz_export") -> bool:
        """
        Exporta las preguntas en diferentes formatos.
        
        Args:
            questions: Lista de preguntas a exportar
            format_type: Tipo de formato (csv, quiz, json)
            base_filename: Nombre base del archivo
            
        Returns:
            True si se exportó correctamente, False en caso contrario
        """
        try:
            if format_type == "quiz":
                return self._export_quiz_format(questions, base_filename)
            elif format_type == "csv":
                return self._export_csv_format(questions, base_filename)
            elif format_type == "json":
                return self._export_json_format(questions, base_filename)
            else:
                raise ValueError(f"Formato no soportado: {format_type}")
        except Exception as e:
            print(f"Error al exportar: {e}")
            return False
    
    def _export_quiz_format(self, questions: List[QuizQuestion], base_filename: str) -> bool:
        """Exporta en formato quiz para aplicaciones."""
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
        
        filename = f"{base_filename}_quiz_format.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(quiz_format, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exportado en formato quiz: {filename}")
        return True
    
    def _export_csv_format(self, questions: List[QuizQuestion], base_filename: str) -> bool:
        """Exporta en formato CSV (solo preguntas de texto)."""
        csv_lines = ["Question,Option1,Option2,Option3,Option4,CorrectAnswer"]
        for q in questions:
            if not q.is_image_question:  # Solo preguntas de texto para CSV
                options = [opt.text or "" for opt in q.options]
                while len(options) < 4:  # Rellenar hasta 4 opciones
                    options.append("")
                
                line = f'"{q.title.text}","{options[0]}","{options[1]}","{options[2]}","{options[3]}",{q.correct_option + 1}'
                csv_lines.append(line)
        
        filename = f"{base_filename}_text_only.csv"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("\n".join(csv_lines))
        
        print(f"✅ Exportado en formato CSV: {filename}")
        return True
    
    def _export_json_format(self, questions: List[QuizQuestion], base_filename: str) -> bool:
        """Exporta en formato JSON nativo de Pydantic."""
        serializable_data = [question.dict() for question in questions]
        
        filename = f"{base_filename}_pydantic.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Exportado en formato JSON: {filename}")
        return True