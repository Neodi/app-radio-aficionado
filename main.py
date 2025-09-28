"""
Script principal usando Clean Architecture simple
"""
def main():
    print("🚀 Ejecutando scraper con Clean Architecture...")
    
    # Importar desde la nueva estructura
    from src.infrastructure.selenium_scrapper import main as scraper_main
    
    # Ejecutar el scraper
    scraper_main()

if __name__ == "__main__":
    main()
