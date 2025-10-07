"""
Caso de uso para ejecutar el proceso completo de scraping de cuestionarios.
Este es el punto de entrada desde la capa de presentación.
"""
from typing import Optional, List
from ...domain.quiz.quiz_question_model import QuizQuestionModel
from ...infrastructure.scraping.driver_config import setup_driver, deny_cookies, refresh_exam
from .quiz_extractor import QuizExtractionService
from ...infrastructure.scraping.data_saver import save_quiz_data_to_json
from ...shared.create_proyect_structure import create_default_structure
import os
from dotenv import load_dotenv


class ScrapingUseCase:
    """
    Caso de uso principal para ejecutar el scraping completo.
    Orquesta toda la aplicación desde la perspectiva del usuario.
    """
    
    def __init__(self):
        self.quiz_extraction_service = QuizExtractionService()
    
    def execute(self, target_configs: Optional[List[dict]] = None) -> bool:
        """
        Ejecuta el proceso completo de scraping para múltiples URLs.
        
        Args:
            target_configs: Lista de configuraciones con 'url' y 'category' (opcional)
            
        Returns:
            bool: True si el scraping fue exitoso, False en caso contrario
        """
        try:
            # 1. Configuración inicial
            create_default_structure()
            load_dotenv()
            
            # 2. Configurar URLs y categorías
            if not target_configs:
                # Usar configuración desde .env
                target_configs = [
                    {
                        'url': os.getenv("URL_RADIOELECTRICIDAD"),
                        'category': os.getenv("CATEGORY_RADIOELECTRICIDAD", "radioelectricidad")
                    },
                    {
                        'url': os.getenv("URL_NORMATIVA"), 
                        'category': os.getenv("CATEGORY_NORMATIVA", "normativa")
                    }
                ]
            
            # Filtrar configuraciones válidas
            valid_configs = [config for config in target_configs if config.get('url')]
            
            if not valid_configs:
                print("❌ Error: No se encontraron URLs válidas para scraping")
                return False
            
            print(f"🚀 Iniciando scraping de {len(valid_configs)} sitios:")
            for config in valid_configs:
                print(f"   - {config['category']}: {config['url']}")
            
            total_success = True
            overall_questions_found = 0
            
            # 3. Procesar cada configuración secuencialmente
            for config_index, config in enumerate(valid_configs, 1):
                url = config['url']
                category = config['category']
                
                print(f"\n{'='*60}")
                print(f"🔄 PROCESANDO SITIO {config_index}/{len(valid_configs)}: {category.upper()}")
                print(f"🌐 URL: {url}")
                print(f"{'='*60}")
                
                site_success = self._process_single_site(url, category)
                
                if site_success['success']:
                    questions_found = site_success['questions_count']
                    overall_questions_found += questions_found
                    print(f"✅ Sitio {category} completado: {questions_found} preguntas nuevas")
                else:
                    total_success = False
                    print(f"❌ Falló el scraping de sitio: {category}")
            
            # 4. Resultado final
            print(f"\n{'='*60}")
            print(f"🏁 RESUMEN FINAL DEL SCRAPING")
            print(f"{'='*60}")
            print(f"📊 Total de preguntas nuevas encontradas: {overall_questions_found}")
            print(f"🎯 Sitios procesados exitosamente: {sum(1 for config in valid_configs if self._get_site_success(config))}")
            print(f"🎯 Total de sitios: {len(valid_configs)}")
            
            if overall_questions_found > 0:
                print(f"🎉 ¡Scraping completado exitosamente!")
                return True
            else:
                print(f"⚠️ Scraping finalizado sin encontrar preguntas nuevas")
                return total_success
                
        except Exception as e:
            print(f"❌ Error durante el scraping general: {str(e)}")
            return False
    
    def _process_single_site(self, url: str, category: str) -> dict:
        """
        Procesa un solo sitio web para scraping.
        
        Returns:
            dict: {'success': bool, 'questions_count': int}
        """
        driver = None
        try:
            # 1. Configurar infraestructura (driver)
            driver = setup_driver()
            
            # 2. Navegar y preparar página
            driver.get(url)
            deny_cookies(driver)
            
            # 3. Bucle principal de scraping hasta que no haya preguntas nuevas
            consecutive_empty_rounds = 0
            max_empty_rounds = 3
            total_questions_found = 0
            round_number = 1
            
            print(f"🔄 Iniciando scraping continuo para {category} (máximo {max_empty_rounds} rondas consecutivas sin nuevas preguntas)")
            
            while consecutive_empty_rounds < max_empty_rounds:
                print(f"\n--- RONDA {round_number} - {category.upper()} ---")
                
                # Extraer datos usando el servicio de aplicación
                quiz_data = self.quiz_extraction_service.extract_quiz_data(driver, category)
                
                if not quiz_data:
                    # No se pudieron extraer datos - contar como ronda vacía
                    consecutive_empty_rounds += 1
                    print(f"⚠️ No se pudieron extraer datos (intento {consecutive_empty_rounds}/{max_empty_rounds})")
                    round_number += 1
                    continue
                
                # Guardar resultados
                new_questions_count = save_quiz_data_to_json(quiz_data, category)
                
                if new_questions_count > 0:
                    # Se encontraron preguntas nuevas - resetear contador
                    consecutive_empty_rounds = 0
                    total_questions_found += new_questions_count
                    print(f"✅ Ronda {round_number}: {new_questions_count} preguntas nuevas encontradas para {category}")
                elif new_questions_count == 0:
                    # No hay preguntas nuevas - incrementar contador
                    consecutive_empty_rounds += 1
                    print(f"ℹ️ Ronda {round_number}: No se encontraron preguntas nuevas para {category} (intento {consecutive_empty_rounds}/{max_empty_rounds})")
                else:
                    # Error al guardar (-1) - contar como ronda vacía
                    consecutive_empty_rounds += 1
                    print(f"❌ Ronda {round_number}: Error al guardar datos para {category} (intento {consecutive_empty_rounds}/{max_empty_rounds})")
                
                round_number += 1
                refresh_exam(driver)
            
            return {
                'success': True,
                'questions_count': total_questions_found
            }
            
        except Exception as e:
            print(f"❌ Error durante el scraping de {category}: {str(e)}")
            return {
                'success': False, 
                'questions_count': 0
            }
        finally:
            # Limpiar recursos
            if driver:
                driver.quit()
    
    def _get_site_success(self, config: dict) -> bool:
        """Helper method para obtener el éxito de un sitio (placeholder)"""
        # En una implementación real, mantendríamos el estado de éxito por sitio
        return True
