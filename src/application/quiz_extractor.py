"""
Módulo para extraer los datos del cuestionario de la página web.
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from ..infrastructure.image_downloader import download_question_image, download_option_images


def extract_question_title(question):
    """Extrae el título de una pregunta."""
    title_element = question.find_element(By.CLASS_NAME, "quiz-question-title")
    return title_element.text.strip()


def is_image_question(question):
    """Determina si una pregunta tiene opciones de imagen."""
    return "quiz-question-has-image-answer" in question.get_attribute("class")


def extract_text_answers(question):
    """Extrae las respuestas de texto de una pregunta normal."""
    answer_labels = question.find_elements(By.CLASS_NAME, "quiz-question-answer-ctrl-lbl")
    return [label.text.strip() for label in answer_labels]


def extract_image_answers(question, question_id):
    """Extrae las respuestas de imagen de una pregunta con opciones de imagen."""
    answer_containers = question.find_elements(By.CLASS_NAME, "quiz-question-answer-holder")
    answers = []
    answer_images = download_option_images(answer_containers, question_id)
    
    for j in range(len(answer_containers)):
        answers.append(f"Opción {j+1}")
    
    return answers, answer_images


def find_correct_answer_text(question, answers):
    """Encuentra la respuesta correcta en preguntas de texto."""
    try:
        correct_element = question.find_element(By.CLASS_NAME, "quiz-question-answer-correct")
        correct_label = correct_element.find_element(By.CLASS_NAME, "quiz-question-answer-ctrl-lbl")
        correct_answer = correct_label.text.strip()
        correct_index = answers.index(correct_answer)
        return correct_answer, correct_index
    except Exception as e:
        print(f"Error encontrando respuesta correcta de texto: {e}")
        return None, None


def find_correct_answer_image(question, answers):
    """Encuentra la respuesta correcta en preguntas de imagen."""
    try:
        all_containers = question.find_elements(By.CLASS_NAME, "quiz-question-answer-holder")
        for idx, container in enumerate(all_containers):
            answer_div = container.find_element(By.CSS_SELECTOR, ".quiz-question-answer")
            if "quiz-question-answer-correct" in answer_div.get_attribute("class"):
                return answers[idx], idx
        return None, None
    except Exception as e:
        print(f"Error encontrando respuesta correcta de imagen: {e}")
        return None, None


def trigger_answer_reveal(question, driver):
    """Hace clic en la primera opción para revelar la respuesta correcta."""
    try:
        first_radio = question.find_element(By.CLASS_NAME, "quiz-question-answer-ctrl")
        driver.execute_script("arguments[0].click();", first_radio)
        time.sleep(0.25)  # Esperar a que se procese la respuesta
    except Exception as e:
        print(f"Error al revelar respuesta: {e}")


def extract_single_question_data(question, question_index, driver):
    """Extrae los datos de una sola pregunta."""
    # Obtener información básica
    question_id = question.get_attribute("data-question-id")
    question_title = extract_question_title(question)
    is_img_question = is_image_question(question)
    
    # Descargar imagen de la pregunta si existe
    question_image = download_question_image(question, question_id)
    
    # Extraer respuestas según el tipo de pregunta
    if is_img_question:
        answers, answer_images = extract_image_answers(question, question_id)
    else:
        answers = extract_text_answers(question)
        answer_images = None
    
    # Revelar la respuesta correcta
    trigger_answer_reveal(question, driver)
    
    # Encontrar la respuesta correcta
    if is_img_question:
        correct_answer, correct_index = find_correct_answer_image(question, answers)
    else:
        correct_answer, correct_index = find_correct_answer_text(question, answers)
    
    # Crear el objeto de datos de la pregunta
    question_data = {
        "question": question_title,
        "answers": answers,
        "correct_answer": correct_answer,
        "correct_index": correct_index,
        "image": question_image,
        "is_image_question": is_img_question,
        "answer_images": answer_images
    }
    
    # Log de progreso
    question_type = 'Imágenes' if is_img_question else 'Texto'
    correct_preview = correct_answer[:30] if correct_answer else 'No encontrada'
    print(f"Pregunta {question_index + 1}: {question_title[:50]}... | Correcta: {correct_preview}... | Tipo: {question_type}")
    
    return question_data


def extract_quiz_data(driver):
    """Extrae todos los datos del cuestionario de la página."""
    try:
        # Esperar a que las preguntas se carguen
        WebDriverWait(driver=driver, timeout=5).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "quiz-question")
            )
        )

        questions = driver.find_elements(By.CLASS_NAME, "quiz-question")
        quiz_data = []

        for i, question in enumerate(questions):
            question_data = extract_single_question_data(question, i, driver)
            quiz_data.append(question_data)

        print(f"\n✅ Extracción completada: {len(quiz_data)} preguntas procesadas")
        return quiz_data

    except Exception as e:
        print(f"❌ Error al extraer las preguntas: {e}")
        return None