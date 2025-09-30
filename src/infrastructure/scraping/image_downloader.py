"""
Módulo para manejar la descarga de imágenes del cuestionario.
"""
import os
import requests
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from src.domain.quiz.quizQuestionModel import QUESTIONS_IMAGE_DIR, OPTIONS_IMAGE_DIR


def download_image(image_url, filename, target_dir):
    """Descarga una imagen desde una URL en el directorio especificado."""
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        
        # Crear directorio si no existe
        os.makedirs(target_dir, exist_ok=True)
        
        filepath = target_dir / filename
        with open(filepath, "wb") as file:
            file.write(response.content)
        
        # print(f"Imagen descargada: {filepath}")
        return True
    except Exception as e:
        print(f"Error al descargar imagen {filename}: {e}")
        return False


def get_image_filename(image_url, question_id, image_type="pregunta", option_index=None):
    """Genera un nombre de archivo único para una imagen."""
    parsed_url = urlparse(image_url)
    file_extension = parsed_url.path.split('.')[-1] if '.' in parsed_url.path else 'png'
    
    if image_type == "pregunta":
        return f"pregunta_{question_id}.{file_extension}"
    elif image_type == "opcion" and option_index is not None:
        return f"pregunta_{question_id}_opcion_{option_index + 1}.{file_extension}"
    else:
        return f"imagen_{question_id}.{file_extension}"


def download_question_image(question, question_id):
    """Descarga la imagen asociada a una pregunta si existe."""
    try:
        image_element = question.find_element(By.CSS_SELECTOR, ".quiz-question-image img")
        image_url = image_element.get_attribute("src")
        
        if image_url:
            image_filename = get_image_filename(image_url, question_id)
            if download_image(image_url, image_filename, QUESTIONS_IMAGE_DIR):
                # Devolver la ruta relativa completa como la espera el modelo
                return str(QUESTIONS_IMAGE_DIR / image_filename).replace("\\", "/")
    except:
        # No hay imagen en esta pregunta
        pass
    
    return None


def download_option_images(answer_containers, question_id):
    """Descarga las imágenes de las opciones de respuesta."""
    answer_images = []
    
    for j, container in enumerate(answer_containers):
        try:
            img_element = container.find_element(By.CSS_SELECTOR, ".quiz-question-answer-image img")
            img_url = img_element.get_attribute("src")
            
            option_filename = get_image_filename(img_url, question_id, "opcion", j)
            
            if download_image(img_url, option_filename, OPTIONS_IMAGE_DIR):
                # Devolver la ruta relativa completa para opciones
                answer_images.append(str(OPTIONS_IMAGE_DIR / option_filename).replace("\\", "/"))
            else:
                answer_images.append(None)
                
        except:
            answer_images.append(None)
    
    return answer_images