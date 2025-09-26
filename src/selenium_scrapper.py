from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
from dotenv import load_dotenv


def setup_driver():
    """Configura y devuelve el driver de Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    service.log_level = 'FATAL'

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def deny_cookies(driver):
    """Rechaza las cookies si el botón está presente."""
    try:
        deny_cookie_button = WebDriverWait(driver=driver, timeout=10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button.fc-cta-do-not-consent")
            )
        )
        deny_cookie_button.click()
        print("$$$$$--- Botón de cookies clickeado exitosamente")
        time.sleep(2)

    except Exception as e:
        print(f"No se pudo hacer clic en el botón de cookies: {e}")

def extract_quiz_data(driver):
    """Extrae los datos del cuestionario de la página."""
    try:
        WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "quiz-question")
            )
        )

        questions = driver.find_elements(By.CLASS_NAME, "quiz-question")
        quiz_data = []

        for i, question in enumerate(questions):
            title_element = question.find_element(By.CLASS_NAME, "quiz-question-title")
            question_title = title_element.text.strip()

            # Extraer todas las respuestas
            answer_labels = question.find_elements(By.CLASS_NAME, "quiz-question-answer-ctrl-lbl")
            answers = [label.text.strip() for label in answer_labels]

            # Hacer clic en la primera opción para revelar la respuesta correcta
            first_radio = question.find_element(By.CLASS_NAME, "quiz-question-answer-ctrl")
            driver.execute_script("arguments[0].click();", first_radio)
            time.sleep(1)  # Esperar a que se procese la respuesta

            # Buscar la respuesta correcta
            correct_answer = None
            try:
                correct_element = question.find_element(By.CLASS_NAME, "quiz-question-answer-correct")
                correct_label = correct_element.find_element(By.CLASS_NAME, "quiz-question-answer-ctrl-lbl")
                correct_answer = correct_label.text.strip()
            except:
                print(f"No se pudo encontrar la respuesta correcta para la pregunta {i+1}")

            question_data = {
                "question": question_title,
                "answers": answers,
                "correct_answer": correct_answer
            }
            quiz_data.append(question_data)
            print(f"Pregunta extraída: {question_title[:50]}... | Correcta: {correct_answer[:30] if correct_answer else 'No encontrada'}...")

        return quiz_data

    except Exception as e:
        print(f"Error al extraer las preguntas: {e}")
        return None

def save_quiz_data_to_json(quiz_data, filename="preguntas/quiz_data.json"):
    """Guarda los datos del cuestionario en un archivo JSON."""
    try:
        json_output = json.dumps(quiz_data, indent=2, ensure_ascii=False)
        # print("\n" + "="*50)
        # print("DATOS EXTRAÍDOS EN JSON:")
        # print("="*50)
        # print(json_output)

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(quiz_data, file, indent=2, ensure_ascii=False)
        print(f"\nDatos guardados en '{filename}'")

    except Exception as e:
        print(f"Error al guardar los datos en JSON: {e}")

def main():
    """Función principal para ejecutar el scraping."""

    load_dotenv()
    URL_BASE = os.getenv("URL_BASE")

    driver = setup_driver()
    driver.get(URL_BASE)
    time.sleep(2)

    deny_cookies(driver)
    quiz_data = extract_quiz_data(driver)

    if quiz_data:
        save_quiz_data_to_json(quiz_data)

    driver.quit()

if __name__ == "__main__":
    main()