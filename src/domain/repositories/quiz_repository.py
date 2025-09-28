"""
Interfaces de repositorio para la capa de dominio.
Estas interfaces definen los contratos que deben implementar las capas de infraestructura.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from ..entities.quiz_question import QuizQuestion

class QuizQuestionRepository(ABC):
    """Interfaz para el repositorio de preguntas de cuestionario."""
    
    @abstractmethod
    def save_questions(self, questions: List[QuizQuestion], filename: str = None) -> bool:
        """
        Guarda una lista de preguntas.
        
        Args:
            questions: Lista de preguntas a guardar
            filename: Nombre del archivo (opcional)
            
        Returns:
            bool: True si se guardaron correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def load_questions(self, filename: str = None) -> List[QuizQuestion]:
        """
        Carga preguntas desde el almacenamiento.
        
        Args:
            filename: Nombre del archivo (opcional)
            
        Returns:
            List[QuizQuestion]: Lista de preguntas cargadas
        """
        pass
    
    @abstractmethod
    def save_questions_legacy_format(self, questions: List[QuizQuestion], filename: str = None) -> bool:
        """
        Guarda preguntas en formato legacy para compatibilidad.
        
        Args:
            questions: Lista de preguntas a guardar
            filename: Nombre del archivo (opcional)
            
        Returns:
            bool: True si se guardaron correctamente, False en caso contrario
        """
        pass

class WebScrapingRepository(ABC):
    """Interfaz para el repositorio de web scraping."""
    
    @abstractmethod
    def extract_quiz_data(self, url: str) -> List[QuizQuestion]:
        """
        Extrae datos de cuestionario desde una URL.
        
        Args:
            url: URL del sitio web a hacer scraping
            
        Returns:
            List[QuizQuestion]: Lista de preguntas extraídas
        """
        pass
    
    @abstractmethod
    def setup_driver(self) -> None:
        """Configura el driver web para hacer scraping."""
        pass
    
    @abstractmethod
    def cleanup_driver(self) -> None:
        """Limpia y cierra el driver web."""
        pass

class ImageRepository(ABC):
    """Interfaz para el repositorio de imágenes."""
    
    @abstractmethod
    def download_image(self, image_url: str, filename: str) -> Optional[str]:
        """
        Descarga una imagen desde una URL.
        
        Args:
            image_url: URL de la imagen
            filename: Nombre del archivo donde guardar
            
        Returns:
            Optional[str]: Ruta del archivo guardado o None si falló
        """
        pass
    
    @abstractmethod
    def download_question_image(self, question_element, question_id: str) -> Optional[str]:
        """
        Descarga la imagen de una pregunta si existe.
        
        Args:
            question_element: Elemento web de la pregunta
            question_id: ID de la pregunta
            
        Returns:
            Optional[str]: Ruta del archivo guardado o None si no hay imagen
        """
        pass
    
    @abstractmethod
    def download_option_images(self, option_elements, question_id: str) -> List[Optional[str]]:
        """
        Descarga las imágenes de las opciones de una pregunta.
        
        Args:
            option_elements: Elementos web de las opciones
            question_id: ID de la pregunta
            
        Returns:
            List[Optional[str]]: Lista de rutas de archivos guardados
        """
        pass