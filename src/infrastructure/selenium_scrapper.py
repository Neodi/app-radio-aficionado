"""
Script principal para hacer scraping del cuestionario de radioaficionados.
Ahora refactorizado en módulos más pequeños y manejables.
"""
import os
from dotenv import load_dotenv
from .driver_config import setup_driver, deny_cookies
from ..application.quiz_extractor import extract_quiz_data
from .data_saver import save_quiz_data_to_json

def main():
    """Función principal para ejecutar el scraping."""

    load_dotenv()
    URL_BASE = os.getenv("URL_BASE")

    driver = setup_driver()
    driver.get(URL_BASE)

    deny_cookies(driver)
    quiz_data = extract_quiz_data(driver)

    if quiz_data:
        save_quiz_data_to_json(quiz_data)

    # input("Presiona Enter para cerrar el navegador...")
    driver.quit()

if __name__ == "__main__":
    main()