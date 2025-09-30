"""
Módulo de infraestructura para extraer elementos específicos de la web usando Selenium.
Contiene toda la lógica específica de UI y navegador.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .image_downloader import download_question_image, download_option_images


class WebElementExtractor:
    """Extractor de elementos web específicos para el quiz."""
    
    @staticmethod
    def extract_question_title(question_element):
        """Extrae el título de una pregunta."""
        title_element = question_element.find_element(By.CLASS_NAME, "quiz-question-title")
        return title_element.text.strip()

    @staticmethod
    def is_image_question(question_element):
        """Determina si una pregunta tiene opciones de imagen."""
        return "quiz-question-has-image-answer" in question_element.get_attribute("class")

    @staticmethod
    def extract_text_answers(question_element):
        """Extrae las respuestas de texto de una pregunta normal."""
        answer_labels = question_element.find_elements(By.CLASS_NAME, "quiz-question-answer-ctrl-lbl")
        return [label.text.strip() for label in answer_labels]

    @staticmethod
    def extract_image_answers(question_element, question_id):
        """Extrae las respuestas de imagen de una pregunta con opciones de imagen."""
        answer_containers = question_element.find_elements(By.CLASS_NAME, "quiz-question-answer-holder")
        answers = []
        answer_images = download_option_images(answer_containers, question_id)
        
        for j in range(len(answer_containers)):
            answers.append(f"Opción {j+1}")
        
        return answers, answer_images

    @staticmethod
    def find_correct_answer_text(question_element, answers):
        """Encuentra la respuesta correcta en preguntas de texto."""
        try:
            correct_element = question_element.find_element(By.CLASS_NAME, "quiz-question-answer-correct")
            correct_label = correct_element.find_element(By.CLASS_NAME, "quiz-question-answer-ctrl-lbl")
            correct_answer = correct_label.text.strip()
            correct_index = answers.index(correct_answer)
            return correct_answer, correct_index
        except Exception as e:
            print(f"Error encontrando respuesta correcta de texto: {e}")
            return None, None

    @staticmethod
    def find_correct_answer_image(question_element, answers):
        """Encuentra la respuesta correcta en preguntas de imagen."""
        try:
            all_containers = question_element.find_elements(By.CLASS_NAME, "quiz-question-answer-holder")
            for idx, container in enumerate(all_containers):
                answer_div = container.find_element(By.CSS_SELECTOR, ".quiz-question-answer")
                if "quiz-question-answer-correct" in answer_div.get_attribute("class"):
                    return answers[idx], idx
            return None, None
        except Exception as e:
            print(f"Error encontrando respuesta correcta de imagen: {e}")
            return None, None

    @staticmethod
    def trigger_answer_reveal(question_element, driver):
        """Hace clic en la primera opción para revelar la respuesta correcta."""
        try:
            first_radio = question_element.find_element(By.CLASS_NAME, "quiz-question-answer-ctrl")
            driver.execute_script("arguments[0].click();", first_radio)
            time.sleep(0.25)  # Esperar a que se procese la respuesta
        except Exception as e:
            print(f"Error al revelar respuesta: {e}")

    @staticmethod
    def get_question_elements(driver):
        """Obtiene todos los elementos de pregunta de la página."""
        try:
            # Esperar a que las preguntas se carguen
            WebDriverWait(driver=driver, timeout=2).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "quiz-question")
                )
            )
            return driver.find_elements(By.CLASS_NAME, "quiz-question")
        except Exception as e:
            print(f"❌ Error al obtener elementos de pregunta: {e}")
            return []

    def extract_raw_question_data(self, question_element, question_index, driver):
        """Extrae datos en bruto de un elemento de pregunta (sin crear modelos de dominio)."""
        # Obtener información básica
        question_id = question_element.get_attribute("data-question-id")
        question_title = self.extract_question_title(question_element)
        is_img_question = self.is_image_question(question_element)
        
        # Descargar imagen de la pregunta si existe
        question_image = download_question_image(question_element, question_id)
        
        # Extraer respuestas según el tipo de pregunta
        if is_img_question:
            answers, answer_images = self.extract_image_answers(question_element, question_id)
        else:
            answers = self.extract_text_answers(question_element)
            answer_images = None
        
        # Revelar la respuesta correcta
        self.trigger_answer_reveal(question_element, driver)
        
        # Encontrar la respuesta correcta
        if is_img_question:
            correct_answer, correct_index = self.find_correct_answer_image(question_element, answers)
        else:
            correct_answer, correct_index = self.find_correct_answer_text(question_element, answers)
        
        # Retornar datos en bruto (sin crear modelos de dominio aquí)
        return {
            'question_id': question_id,
            'question_title': question_title,
            'question_image': question_image,
            'is_img_question': is_img_question,
            'answers': answers,
            'answer_images': answer_images,
            'correct_answer': correct_answer,
            'correct_index': correct_index,
            'question_index': question_index
        }