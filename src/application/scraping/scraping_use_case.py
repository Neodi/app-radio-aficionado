"""
Caso de uso para ejecutar el proceso completo de scraping de cuestionarios.
Este es el punto de entrada desde la capa de presentación.
"""
from typing import Optional, List
from ...domain.quiz.quizQuestionModel import QuizQuestion
from ...infrastructure.scraping.driver_config import setup_driver, deny_cookies, refresh_exam
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
                
                # 4. Bucle principal de scraping hasta que no haya preguntas nuevas
                consecutive_empty_rounds = 0
                max_empty_rounds = 3
                total_questions_found = 0
                round_number = 1
                
                print(f"🔄 Iniciando scraping continuo (máximo {max_empty_rounds} rondas consecutivas sin nuevas preguntas)")
                
                while consecutive_empty_rounds < max_empty_rounds:
                    print(f"\n--- RONDA {round_number} ---")
                    
                    # Extraer datos usando el servicio de aplicación
                    quiz_data = self.quiz_extraction_service.extract_quiz_data(driver)
                    
                    if not quiz_data:
                        # No se pudieron extraer datos - contar como ronda vacía
                        consecutive_empty_rounds += 1
                        print(f"⚠️ No se pudieron extraer datos (intento {consecutive_empty_rounds}/{max_empty_rounds})")
                        round_number += 1
                        continue
                    
                    # Guardar resultados
                    new_questions_count = save_quiz_data_to_json(quiz_data)
                    
                    if new_questions_count > 0:
                        # Se encontraron preguntas nuevas - resetear contador
                        consecutive_empty_rounds = 0
                        total_questions_found += new_questions_count
                        print(f"✅ Ronda {round_number}: {new_questions_count} preguntas nuevas encontradas")
                    elif new_questions_count == 0:
                        # No hay preguntas nuevas - incrementar contador
                        consecutive_empty_rounds += 1
                        print(f"ℹ️ Ronda {round_number}: No se encontraron preguntas nuevas (intento {consecutive_empty_rounds}/{max_empty_rounds})")
                    else:
                        # Error al guardar (-1) - contar como ronda vacía
                        consecutive_empty_rounds += 1
                        print(f"❌ Ronda {round_number}: Error al guardar datos (intento {consecutive_empty_rounds}/{max_empty_rounds})")
                    
                    round_number += 1
                    refresh_exam(driver)


                
                # 5. Resultado final
                if total_questions_found > 0:
                    print(f"\n🎉 Scraping completado exitosamente!")
                    print(f"📊 Total de preguntas nuevas encontradas: {total_questions_found}")
                    print(f"🔄 Rondas ejecutadas: {round_number - 1}")
                    return True
                else:
                    print(f"\n⚠️ Scraping finalizado sin encontrar preguntas nuevas")
                    print(f"🔄 Rondas ejecutadas: {round_number - 1}")
                    return False
                    
            finally:
                # 6. Limpiar recursos
                driver.quit()
                
        except Exception as e:
            print(f"❌ Error durante el scraping: {str(e)}")
            return False
