"""
Script principal para hacer scraping del cuestionario de radioaficionados.
Ahora refactorizado en módulos más pequeños y manejables con soporte para Pydantic.
"""
import os
from dotenv import load_dotenv
from driver_config import setup_driver, deny_cookies
from quiz_extractor import extract_quiz_data
from data_saver import save_quiz_data_to_json, save_quiz_data_legacy_format, print_quiz_summary

def main():
    """Función principal para ejecutar el scraping con soporte Pydantic."""

    load_dotenv()
    URL_BASE = os.getenv("URL_BASE")

    driver = setup_driver()
    driver.get(URL_BASE)

    deny_cookies(driver)
    quiz_data = extract_quiz_data(driver)

    if quiz_data:
        # Guardar en formato Pydantic (nuevo)
        save_quiz_data_to_json(quiz_data)
        
        # Guardar en formato legacy para compatibilidad
        save_quiz_data_legacy_format(quiz_data)
        
        # Mostrar resumen
        print_quiz_summary(quiz_data)

    # input("Presiona Enter para cerrar el navegador...")
    driver.quit()

if __name__ == "__main__":
    main()