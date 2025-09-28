"""
Implementación del web scraper usando Selenium.
Esta clase implementa la interfaz WebScrapingRepository.
"""
import time
from typing import List
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from ...domain.entities.quiz_question import QuizQuestion, Title, Option
from ...domain.repositories.quiz_repository import WebScrapingRepository
from .driver_config import WebDriverConfig
from .image_downloader import SeleniumImageRepository

class SeleniumWebScrapingRepository(WebScrapingRepository):
    """Implementación del web scraper usando Selenium."""
    
    def __init__(self):
        """Inicializa el repositorio de web scraping."""
        self.driver = None
        self.image_repo = SeleniumImageRepository()
    
    def setup_driver(self) -> None:
        """Configura el driver web para hacer scraping."""
        self.driver = WebDriverConfig.setup_driver()
    
    def cleanup_driver(self) -> None:
        """Limpia y cierra el driver web."""
        if self.driver:
            WebDriverConfig.cleanup_driver(self.driver)
            self.driver = None
    
    def extract_quiz_data(self, url: str) -> List[QuizQuestion]:
        """
        Extrae datos de cuestionario desde una URL.
        
        Args:
            url: URL del sitio web a hacer scraping
            
        Returns:
            Lista de preguntas extraídas
        """
        if not self.driver:
            raise RuntimeError("Driver no configurado. Llama a setup_driver() primero.")
        
        try:
            # Navegar a la URL
            self.driver.get(url)
            
            # Rechazar cookies
            WebDriverConfig.deny_cookies(self.driver)
            
            # Extraer preguntas
            return self._extract_all_questions()
            
        except Exception as e:
            print(f"❌ Error al extraer las preguntas: {e}")
            return []
    
    def _extract_all_questions(self) -> List[QuizQuestion]:
        """Extrae todas las preguntas de la página."""
        try:
            # Esperar a que las preguntas se carguen
            WebDriverWait(driver=self.driver, timeout=5).until(
                EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "quiz-question")
                )
            )

            questions = self.driver.find_elements(By.CLASS_NAME, "quiz-question")
            quiz_data = []

            for i, question in enumerate(questions):
                question_data = self._extract_single_question(question, i)
                if question_data:
                    quiz_data.append(question_data)

            print(f"\n✅ Extracción completada: {len(quiz_data)} preguntas procesadas")
            return quiz_data

        except Exception as e:
            print(f"❌ Error al extraer las preguntas: {e}")
            return []
    
    def _extract_single_question(self, question_element, question_index: int) -> QuizQuestion:
        """Extrae los datos de una sola pregunta."""
        try:
            # Obtener información básica
            question_id = question_element.get_attribute("data-question-id")
            question_title = self._extract_question_title(question_element)
            is_img_question = self._is_image_question(question_element)
            
            # Descargar imagen de la pregunta si existe
            question_image = self.image_repo.download_question_image(question_element, question_id)
            
            # Extraer respuestas según el tipo de pregunta
            if is_img_question:
                answers, answer_images = self._extract_image_answers(question_element, question_id)
            else:
                answers = self._extract_text_answers(question_element)
                answer_images = None
            
            # Revelar la respuesta correcta
            self._trigger_answer_reveal(question_element)
            
            # Encontrar la respuesta correcta
            if is_img_question:
                correct_answer, correct_index = self._find_correct_answer_image(question_element, answers)
            else:
                correct_answer, correct_index = self._find_correct_answer_text(question_element, answers)
            
            # Crear el título usando el modelo Pydantic
            title = Title(text=question_title, image=question_image)
            
            # Crear las opciones usando el modelo Pydantic
            options = []
            for i, answer in enumerate(answers):
                option_image = None
                if is_img_question and answer_images and i < len(answer_images):
                    option_image = answer_images[i]
                
                options.append(Option(text=answer, image=option_image))
            
            # Asegurar que tenemos un índice válido
            if correct_index is None or correct_index < 0 or correct_index >= len(options):
                print(f"⚠️ Advertencia: Índice de respuesta correcta inválido para pregunta {question_index + 1}")
                correct_index = 0  # Fallback al primer índice
            
            # Crear el objeto QuizQuestion usando Pydantic
            quiz_question = QuizQuestion(
                original_id=question_id,
                title=title,
                options=options,
                correct_option=correct_index,
                is_image_question=is_img_question
            )
            
            # Log de progreso
            question_type = 'Imágenes' if is_img_question else 'Texto'
            correct_preview = correct_answer[:30] if correct_answer else 'No encontrada'
            print(f"Pregunta {question_index + 1}: {question_title[:50]}... | Correcta: {correct_preview}... | Tipo: {question_type}")
            
            return quiz_question
            
        except Exception as e:
            print(f"❌ Error creando objeto QuizQuestion para pregunta {question_index + 1}: {e}")
            # Fallback: crear un objeto mínimo válido
            fallback_options = [Option(text=f"Opción {i+1}", image=None) for i in range(2)]
            return QuizQuestion(
                original_id=question_id or f"fallback_{question_index}",
                title=Title(text=question_title or "Pregunta sin título", image=None),
                options=fallback_options,
                correct_option=0,
                is_image_question=False
            )
    
    def _extract_question_title(self, question_element) -> str:
        """Extrae el título de una pregunta."""
        try:
            title_element = question_element.find_element(By.CLASS_NAME, "quiz-question-title")
            return title_element.text.strip()
        except Exception:
            return "Pregunta sin título"
    
    def _is_image_question(self, question_element) -> bool:
        """Determina si una pregunta tiene opciones de imagen."""
        return "quiz-question-has-image-answer" in question_element.get_attribute("class")
    
    def _extract_text_answers(self, question_element) -> List[str]:
        """Extrae las respuestas de texto de una pregunta normal."""
        try:
            answer_labels = question_element.find_elements(By.CLASS_NAME, "quiz-question-answer-ctrl-lbl")
            return [label.text.strip() for label in answer_labels]
        except Exception:
            return []
    
    def _extract_image_answers(self, question_element, question_id: str) -> tuple:
        """Extrae las respuestas de imagen de una pregunta con opciones de imagen."""
        try:
            answer_containers = question_element.find_elements(By.CLASS_NAME, "quiz-question-answer-holder")
            answers = []
            answer_images = self.image_repo.download_option_images(answer_containers, question_id)
            
            for j in range(len(answer_containers)):
                answers.append(f"Opción {j+1}")
            
            return answers, answer_images
        except Exception:
            return [], None
    
    def _find_correct_answer_text(self, question_element, answers: List[str]) -> tuple:
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
    
    def _find_correct_answer_image(self, question_element, answers: List[str]) -> tuple:
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
    
    def _trigger_answer_reveal(self, question_element) -> None:
        """Hace clic en la primera opción para revelar la respuesta correcta."""
        try:
            first_radio = question_element.find_element(By.CLASS_NAME, "quiz-question-answer-ctrl")
            self.driver.execute_script("arguments[0].click();", first_radio)
            time.sleep(0.25)  # Esperar a que se procese la respuesta
        except Exception as e:
            print(f"Error al revelar respuesta: {e}")