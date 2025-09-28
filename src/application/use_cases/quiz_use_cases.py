"""
Casos de uso para la extracción de cuestionarios.
Esta capa contiene la lógica de negocio de la aplicación.
"""
from typing import List, Dict, Optional
from ..services.quiz_service import QuizService
from ...domain.entities.quiz_question import QuizQuestion
from ...domain.repositories.quiz_repository import QuizQuestionRepository, WebScrapingRepository

class ExtractQuizUseCase:
    """Caso de uso para extraer preguntas de cuestionario desde una fuente web."""
    
    def __init__(
        self,
        web_scraping_repository: WebScrapingRepository,
        quiz_repository: QuizQuestionRepository,
        quiz_service: QuizService
    ):
        self.web_scraping_repository = web_scraping_repository
        self.quiz_repository = quiz_repository
        self.quiz_service = quiz_service
    
    def execute(self, url: str, save_legacy: bool = True) -> Dict[str, any]:
        """
        Ejecuta la extracción completa del cuestionario.
        
        Args:
            url: URL del sitio web a hacer scraping
            save_legacy: Si guardar también en formato legacy
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            # Configurar el scraper
            self.web_scraping_repository.setup_driver()
            
            # Extraer datos
            questions = self.web_scraping_repository.extract_quiz_data(url)
            
            if not questions:
                return {
                    "success": False,
                    "error": "No se pudieron extraer preguntas",
                    "questions": []
                }
            
            # Validar datos
            validation_result = self.quiz_service.validate_questions(questions)
            if not validation_result["is_valid"]:
                print("⚠️ Advertencias en la validación:")
                for error in validation_result["errors"]:
                    print(f"  - {error}")
            
            # Guardar en formato Pydantic
            save_success = self.quiz_repository.save_questions(questions)
            
            # Guardar en formato legacy si se solicita
            legacy_success = True
            if save_legacy:
                legacy_success = self.quiz_repository.save_questions_legacy_format(questions)
            
            # Obtener estadísticas
            stats = self.quiz_service.get_statistics(questions)
            
            return {
                "success": save_success and legacy_success,
                "questions": questions,
                "statistics": stats,
                "validation": validation_result,
                "total_questions": len(questions)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "questions": []
            }
        finally:
            # Limpiar recursos
            self.web_scraping_repository.cleanup_driver()

class LoadQuizUseCase:
    """Caso de uso para cargar preguntas desde almacenamiento."""
    
    def __init__(self, quiz_repository: QuizQuestionRepository, quiz_service: QuizService):
        self.quiz_repository = quiz_repository
        self.quiz_service = quiz_service
    
    def execute(self, filename: str = None) -> Dict[str, any]:
        """
        Ejecuta la carga de preguntas.
        
        Args:
            filename: Nombre del archivo a cargar (opcional)
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            questions = self.quiz_repository.load_questions(filename)
            
            if not questions:
                return {
                    "success": False,
                    "error": "No se encontraron preguntas",
                    "questions": []
                }
            
            stats = self.quiz_service.get_statistics(questions)
            
            return {
                "success": True,
                "questions": questions,
                "statistics": stats,
                "total_questions": len(questions)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "questions": []
            }

class SearchQuizUseCase:
    """Caso de uso para buscar preguntas."""
    
    def __init__(self, quiz_service: QuizService):
        self.quiz_service = quiz_service
    
    def execute(self, questions: List[QuizQuestion], search_term: str) -> Dict[str, any]:
        """
        Ejecuta la búsqueda de preguntas.
        
        Args:
            questions: Lista de preguntas donde buscar
            search_term: Término de búsqueda
            
        Returns:
            Dict con el resultado de la búsqueda
        """
        try:
            results = self.quiz_service.search_questions(questions, search_term)
            
            return {
                "success": True,
                "results": results,
                "total_found": len(results),
                "search_term": search_term
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "results": []
            }

class FilterQuizUseCase:
    """Caso de uso para filtrar preguntas por criterios."""
    
    def __init__(self, quiz_service: QuizService):
        self.quiz_service = quiz_service
    
    def execute_by_type(self, questions: List[QuizQuestion], is_image_question: bool) -> Dict[str, any]:
        """
        Filtra preguntas por tipo.
        
        Args:
            questions: Lista de preguntas a filtrar
            is_image_question: True para preguntas con imágenes, False para texto
            
        Returns:
            Dict con el resultado del filtrado
        """
        try:
            filtered = self.quiz_service.filter_by_type(questions, is_image_question)
            
            return {
                "success": True,
                "questions": filtered,
                "total_filtered": len(filtered),
                "filter_type": "imagen" if is_image_question else "texto"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "questions": []
            }

class ExportQuizUseCase:
    """Caso de uso para exportar preguntas en diferentes formatos."""
    
    def __init__(self, quiz_service: QuizService):
        self.quiz_service = quiz_service
    
    def execute(self, questions: List[QuizQuestion], format_type: str, filename: str = None) -> Dict[str, any]:
        """
        Ejecuta la exportación de preguntas.
        
        Args:
            questions: Lista de preguntas a exportar
            format_type: Tipo de formato (csv, quiz, json)
            filename: Nombre base del archivo
            
        Returns:
            Dict con el resultado de la exportación
        """
        try:
            success = self.quiz_service.export_questions(questions, format_type, filename)
            
            return {
                "success": success,
                "format": format_type,
                "filename": filename,
                "total_exported": len(questions) if success else 0
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }