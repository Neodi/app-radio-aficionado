"""
Servicio de aplicación para extraer datos del cuestionario.
Orquesta la extracción web y la creación de modelos de dominio.
"""

from typing import List, Optional

from ...domain.quiz.quiz_question_factory import QuizQuestionFactory
from ...domain.quiz.quiz_question_model import QuizQuestionModel
from ...infrastructure.scraping.web_element_extractor import WebElementExtractor


class QuizExtractionService:
    """Servicio de aplicación para extraer y procesar cuestionarios."""

    def __init__(self):
        """Inicializa el servicio con los componentes necesarios."""
        self.web_extractor = WebElementExtractor()
        self.question_factory = QuizQuestionFactory()

    def extract_single_question_data(
        self, question_element, question_index, driver, category: str = "default"
    ) -> QuizQuestionModel:
        """
        Extrae y procesa una sola pregunta.
        Orquesta entre infraestructura (extracción web) y dominio (creación de modelos).
        """
        # 1. Extraer datos en bruto usando infraestructura
        raw_data = self.web_extractor.extract_raw_question_data(
            question_element, question_index, driver, category
        )

        # 2. Crear modelo de dominio usando factory
        quiz_question = self.question_factory.create_quiz_question(
            question_title=raw_data["question_title"],
            question_image=raw_data["question_image"],
            answers=raw_data["answers"],
            answer_images=raw_data["answer_images"],
            correct_index=raw_data["correct_index"],
            is_img_question=raw_data["is_img_question"],
            question_index=raw_data["question_index"],
            category=category,
        )

        # 3. Log de progreso
        # question_type = "Imágenes" if raw_data["is_img_question"] else "Texto"
        # correct_preview = (
        #     raw_data["correct_answer"][:30]
        #     if raw_data["correct_answer"]
        #     else "No encontrada"
        # )
        # print(f"Pregunta {question_index + 1}: {raw_data['question_title'][:50]}... | Correcta: {correct_preview}... | Tipo: {question_type}")

        return quiz_question

    def extract_quiz_data(
        self, driver, category: str = "default"
    ) -> Optional[List[QuizQuestionModel]]:
        """
        Extrae todos los datos del cuestionario de la página.
        Punto de entrada principal del servicio.
        """
        try:
            # 1. Obtener elementos web
            question_elements = self.web_extractor.get_question_elements(driver)

            if not question_elements:
                print("❌ No se encontraron elementos de pregunta")
                return None

            # 2. Procesar cada pregunta
            quiz_data = []
            for i, question_element in enumerate(question_elements):
                question_data = self.extract_single_question_data(
                    question_element, i, driver, category
                )
                quiz_data.append(question_data)

            print(
                f"\n✅ Extracción completada: {len(quiz_data)} preguntas procesadas para categoría '{category}'"
            )
            return quiz_data

        except Exception as e:
            print(f"❌ Error al extraer las preguntas: {e}")
            return None


# Función de conveniencia para mantener compatibilidad con código existente
def extract_quiz_data(
    driver, category: str = "default"
) -> Optional[List[QuizQuestionModel]]:
    """Función de conveniencia que usa el servicio de aplicación."""
    service = QuizExtractionService()
    return service.extract_quiz_data(driver, category)
