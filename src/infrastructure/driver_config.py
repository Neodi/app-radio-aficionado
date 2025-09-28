"""
Módulo para configurar y manejar el driver de Chrome de forma simple.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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