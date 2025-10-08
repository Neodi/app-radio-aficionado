"""
Módulo para configurar y manejar el driver de Chrome de forma simple.
"""

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """Configura y devuelve el driver de Chrome básico."""
    chrome_options = Options()

    # Solo las configuraciones mínimas necesarias
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-smooth-scrolling")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver


def deny_cookies(driver):
    """Rechaza las cookies si el botón está presente."""
    try:
        deny_cookie_button = WebDriverWait(driver=driver, timeout=3).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.fc-cta-do-not-consent")
            )
        )
        deny_cookie_button.click()

    except Exception as e:
        print(f"No se pudo hacer clic en el botón de cookies: {e}")


def refresh_exam(
    driver,
):
    """Hace clic en 'Realizar nuevo examen' para refrescar la página."""
    try:
        # Buscar el botón por su texto y clase
        new_exam_button = driver.find_element(
            By.XPATH,
            "//a[contains(@href, '/examenes/') and .//div[@class='mio6' and contains(text(), 'Realizar nuevo examen')]]",
        )

        # Hacer clic en el botón
        driver.execute_script("arguments[0].click();", new_exam_button)
        print("🔄 Navegando a nuevo examen...")

        # Esperar a que cargue la nueva página
        time.sleep(1)

        # # Opcional: Verificar que se cargó correctamente
        # driver.implicitly_wait(5)

    except Exception as e:
        print(f"⚠️ Error al hacer clic en 'Realizar nuevo examen': {e}")
        print("⚠️ Continuando con la siguiente ronda...")
