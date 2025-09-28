"""
Interfaz de línea de comandos para el scraper de cuestionarios.
Esta es la capa de presentación que orquesta los casos de uso.
"""
import os
from dotenv import load_dotenv

# Importar casos de uso y repositorios
from ...application.use_cases.quiz_use_cases import ExtractQuizUseCase, LoadQuizUseCase, ExportQuizUseCase
from ...application.services.quiz_service import QuizService
from ...infrastructure.repositories.json_quiz_repository import JsonQuizQuestionRepository
from ...infrastructure.web_scraping.selenium_scraper import SeleniumWebScrapingRepository

class QuizScraperCLI:
    """Interfaz de línea de comandos para el scraper."""
    
    def __init__(self):
        """Inicializa la CLI con todas las dependencias."""
        # Configurar repositorios (capa de infraestructura)
        self.quiz_repository = JsonQuizQuestionRepository()
        self.web_scraping_repository = SeleniumWebScrapingRepository()
        
        # Configurar servicios (capa de aplicación)
        self.quiz_service = QuizService()
        
        # Configurar casos de uso (capa de aplicación)
        self.extract_use_case = ExtractQuizUseCase(
            self.web_scraping_repository,
            self.quiz_repository,
            self.quiz_service
        )
        self.load_use_case = LoadQuizUseCase(
            self.quiz_repository,
            self.quiz_service
        )
        self.export_use_case = ExportQuizUseCase(self.quiz_service)
    
    def run_scraping(self):
        """Ejecuta el proceso completo de scraping."""
        print("🚀 Iniciando scraper de cuestionarios de radioaficionados...")
        
        # Cargar configuración
        load_dotenv()
        url = os.getenv("URL_BASE")
        
        if not url:
            print("❌ Error: URL_BASE no configurada en .env")
            return False
        
        # Ejecutar extracción
        result = self.extract_use_case.execute(url, save_legacy=True)
        
        if result["success"]:
            print(f"\n🎉 ¡Extracción exitosa! {result['total_questions']} preguntas procesadas")
            
            # Mostrar estadísticas
            stats = result["statistics"]
            print("\n📊 Estadísticas:")
            for key, value in stats.items():
                print(f"  • {key}: {value}")
            
            # Mostrar resumen
            self._print_quiz_summary(result["questions"])
            
            # Exportar en diferentes formatos
            print("\n📤 Exportando en diferentes formatos...")
            self._export_formats(result["questions"])
            
        else:
            print(f"❌ Error en la extracción: {result.get('error', 'Error desconocido')}")
            return False
        
        return True
    
    def run_load_and_analyze(self, filename: str = None):
        """Carga y analiza preguntas existentes."""
        print("📖 Cargando preguntas existentes...")
        
        result = self.load_use_case.execute(filename)
        
        if result["success"]:
            print(f"✅ Preguntas cargadas: {result['total_questions']}")
            
            # Mostrar estadísticas
            stats = result["statistics"]
            print("\n📊 Estadísticas:")
            for key, value in stats.items():
                print(f"  • {key}: {value}")
            
            return result["questions"]
        else:
            print(f"❌ Error al cargar: {result.get('error', 'Error desconocido')}")
            return []
    
    def _print_quiz_summary(self, questions):
        """Imprime un resumen de las preguntas."""
        if not questions:
            print("❌ No hay preguntas que mostrar")
            return
        
        print("\n" + "="*60)
        print("📋 RESUMEN DEL CUESTIONARIO EXTRAÍDO")
        print("="*60)
        
        for i, question in enumerate(questions[:5], 1):  # Mostrar solo las primeras 5
            print(f"\n{i}. {question.title.text[:80]}...")
            print(f"   ID: {question.id}")
            if question.original_id:
                print(f"   ID Original: {question.original_id}")
            print(f"   Tipo: {'🖼️ Imágenes' if question.is_image_question else '📝 Texto'}")
            
            # Mostrar opciones
            for j, option in enumerate(question.options):
                marker = "✅" if j == question.correct_option else "  "
                print(f"   {marker} Opción {j+1}: {option.text[:50]}...")
                if option.image:
                    print(f"       Imagen: {option.image}")
            
            if question.title.image:
                print(f"   Imagen de pregunta: {question.title.image}")
        
        if len(questions) > 5:
            print(f"\n... y {len(questions) - 5} preguntas más")
        
        print("="*60)
    
    def _export_formats(self, questions):
        """Exporta las preguntas en diferentes formatos."""
        formats_to_export = ["quiz", "csv", "json"]
        
        for format_type in formats_to_export:
            result = self.export_use_case.execute(
                questions, 
                format_type, 
                "preguntas/quiz_export"
            )
            
            if result["success"]:
                print(f"  ✅ Exportado en formato {format_type}")
            else:
                print(f"  ❌ Error exportando {format_type}: {result.get('error', 'Error desconocido')}")

def main():
    """Función principal de la CLI."""
    cli = QuizScraperCLI()
    
    print("🔧 Quiz Scraper - Clean Architecture")
    print("=" * 40)
    
    try:
        # Ejecutar scraping
        success = cli.run_scraping()
        
        if success:
            print("\n✨ ¡Proceso completado exitosamente!")
        else:
            print("\n💥 El proceso falló")
            
    except KeyboardInterrupt:
        print("\n⚠️ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n💥 Error inesperado: {e}")

if __name__ == "__main__":
    main()