"""
Configuración del driver de Selenium para web scraping.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebDriverConfig:
    """Configurador del driver web."""
    
    @staticmethod
    def setup_driver():
        """Configura y retorna el driver de Chrome."""
        options = Options()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    
    @staticmethod
    def deny_cookies(driver):
        """Rechaza las cookies del sitio web."""
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "CybotCookiebotDialogBodyButtonDecline"))
            ).click()
            print("✅ Cookies rechazadas")
        except Exception as e:
            print(f"⚠️ No se pudo rechazar cookies o no aparecieron: {e}")
    
    @staticmethod
    def cleanup_driver(driver):
        """Cierra y limpia el driver."""
        if driver:
            driver.quit()