"""
Factory del dominio para crear objetos QuizQuestion validados.
Contiene la lógica de creación y validación de entidades de dominio.
"""
from typing import List, Optional
from .quizQuestionModel import QuizQuestion, Title, Option


class QuizQuestionFactory:
    """Factory para crear objetos QuizQuestion validados y consistentes."""
    
    @staticmethod
    def create_quiz_question(
        question_title: str,
        question_image: Optional[str],
        answers: List[str],
        answer_images: Optional[List[str]],
        correct_index: Optional[int],
        is_img_question: bool = False,
        question_index: int = 0
    ) -> QuizQuestion:
        """
        Crea un objeto QuizQuestion validado a partir de datos en bruto.
        
        Args:
            question_title: Texto de la pregunta
            question_image: URL/path de imagen de pregunta (opcional)
            answers: Lista de textos de respuestas
            answer_images: Lista de URLs/paths de imágenes de respuestas (opcional)
            correct_index: Índice de la respuesta correcta
            is_img_question: Si es pregunta con imágenes
            question_index: Índice de la pregunta (para logging)
            
        Returns:
            QuizQuestion: Objeto validado del dominio
        """
        # Crear el título usando el modelo de dominio
        title = Title(
            titleText=question_title,
            titleImage=question_image
        )
        
        # Crear las opciones usando el modelo de dominio
        options = []
        for i, answer in enumerate(answers):
            option_image = None
            if is_img_question and answer_images and i < len(answer_images):
                option_image = answer_images[i]
            
            options.append(Option(
                optionText=answer,
                optionImage=option_image
            ))
        
        # Validar y asegurar que tenemos un índice correcto válido
        validated_correct_index = QuizQuestionFactory._validate_correct_index(
            correct_index, len(options), question_index
        )
        
        # Crear el objeto QuizQuestion usando Pydantic con manejo de errores
        try:
            quiz_question = QuizQuestion(
                title=title,
                options=options,
                correct_option=validated_correct_index
            )
            
            return quiz_question
            
        except Exception as e:
            print(f"❌ Error creando objeto QuizQuestion para pregunta {question_index + 1}: {e}")
            # Fallback: crear un objeto mínimo válido
            return QuizQuestionFactory._create_fallback_question(
                question_title, question_image, answers
            )
    
    @staticmethod
    def _validate_correct_index(correct_index: Optional[int], num_options: int, question_index: int) -> int:
        """Valida y corrige el índice de respuesta correcta."""
        if correct_index is None or correct_index < 0 or correct_index >= num_options:
            print(f"⚠️ Advertencia: Índice de respuesta correcta inválido para pregunta {question_index + 1}")
            return 0  # Fallback al primer índice
        return correct_index
    
    @staticmethod
    def _create_fallback_question(
        question_title: str, 
        question_image: Optional[str], 
        answers: List[str]
    ) -> QuizQuestion:
        """Crea un objeto QuizQuestion de fallback cuando falla la creación normal."""
        fallback_options = [
            Option(optionText=f"Opción {i+1}", optionImage=None) 
            for i in range(max(2, len(answers)))
        ]
        
        return QuizQuestion(
            title=Title(
                titleText=question_title or "Pregunta sin título", 
                titleImage=question_image
            ),
            options=fallback_options,
            correct_option=0
        )