"""
Caso de uso para ejecutar el proceso completo de scraping de cuestionarios.
Este es el punto de entrada desde la capa de presentación.
"""
from typing import Optional, List
from ...domain.quiz.quizQuestionModel import QuizQuestion
from ...infrastructure.scraping.driver_config import setup_driver, deny_cookies
from .quiz_extractor import QuizExtractionService
from ...infrastructure.scraping.data_saver import save_quiz_data_to_json
from ...shared.create_proyect_structure import create_project_structure
import os
from dotenv import load_dotenv


class ScrapingUseCase:
    """
    Caso de uso principal para ejecutar el scraping completo.
    Orquesta toda la aplicación desde la perspectiva del usuario.
    """
    
    def __init__(self):
        self.quiz_extraction_service = QuizExtractionService()
    
    def execute(self, url: Optional[str] = None) -> bool:
        """
        Ejecuta el proceso completo de scraping.
        
        Args:
            url: URL a scrapear (opcional, usa .env si no se proporciona)
            
        Returns:
            bool: True si el scraping fue exitoso, False en caso contrario
        """
        try:
            # 1. Configuración inicial
            create_project_structure()
            load_dotenv()
            target_url = url or os.getenv("URL_BASE")
            
            if not target_url:
                print("❌ Error: No se encontró URL_BASE en .env ni se proporcionó URL")
                return False
            
            print(f"🚀 Iniciando scraping de: {target_url}")
            
            # 2. Configurar infraestructura (driver)
            driver = setup_driver()
            
            try:
                # 3. Navegar y preparar página
                driver.get(target_url)
                deny_cookies(driver)
                
                # 4. Extraer datos usando el servicio de aplicación
                quiz_data = self.quiz_extraction_service.extract_quiz_data(driver)
                
                # 5. Guardar resultados
                if quiz_data:
                    success = save_quiz_data_to_json(quiz_data)
                    if success:
                        print(f"✅ Scraping completado exitosamente: {len(quiz_data)} preguntas extraídas")
                        return True
                    else:
                        print("❌ Error al guardar los datos")
                        return False
                else:
                    print("❌ No se pudieron extraer datos del cuestionario")
                    return False
                    
            finally:
                # 6. Limpiar recursos
                driver.quit()
                
        except Exception as e:
            print(f"❌ Error durante el scraping: {str(e)}")
            return False
