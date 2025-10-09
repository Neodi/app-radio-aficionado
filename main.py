"""
Punto de entrada de la aplicación que usa casos de uso.
"""

import sys


def main():
    """Función principal que orquesta la aplicación."""

    if len(sys.argv) < 2:
        print("🚀 Radio Amateur Quiz Scraper - Clean Architecture")
        print("\nUso:")
        print("  python main.py scraping [url]    # Ejecutar scraping")
        print("  python main.py help              # Mostrar ayuda")
        return

    command = sys.argv[1]

    if command == "scraping":
        print("🕷️ Ejecutando caso de uso de scraping...")

        # Usar el Use Case de la capa de aplicación
        from src.application.scraping.scraping_use_case import ScrapingUseCase

        # URL opcional como parámetro
        url = sys.argv[2] if len(sys.argv) > 2 else None

        # Ejecutar caso de uso
        use_case = ScrapingUseCase()
        target_configs = [] if url is None else [{"url": url}]
        success = use_case.execute(target_configs)

        if success:
            print("🎉 ¡Scraping completado exitosamente!")
        else:
            print("❌ El scraping falló. Revisa los logs para más detalles.")

    elif command == "help":
        print("📖 Ayuda de Radio Amateur Quiz Scraper")
        print("\nComandos disponibles:")
        print("  scraping [url] - Ejecuta el scraping del cuestionario")
        print("                   URL es opcional (usa .env si no se especifica)")
        print("  help          - Muestra esta ayuda")

    else:
        print(f"❌ Comando '{command}' no reconocido")
        print("Usa 'python main.py help' para ver comandos disponibles")


if __name__ == "__main__":
    main()
