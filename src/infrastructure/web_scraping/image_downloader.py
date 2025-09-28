"""
Descarga de imágenes para preguntas y opciones del cuestionario.
"""
import os
import requests
from typing import List, Optional
from selenium.webdriver.common.by import By
from ...domain.repositories.quiz_repository import ImageRepository

class SeleniumImageRepository(ImageRepository):
    """Implementación del repositorio de imágenes usando Selenium."""
    
    def __init__(self, base_path: str = "preguntas/imagenes"):
        """
        Inicializa el repositorio de imágenes.
        
        Args:
            base_path: Ruta base donde guardar las imágenes
        """
        self.base_path = base_path
    
    def download_image(self, image_url: str, filename: str) -> Optional[str]:
        """
        Descarga una imagen desde una URL.
        
        Args:
            image_url: URL de la imagen
            filename: Nombre del archivo donde guardar
            
        Returns:
            Ruta del archivo guardado o None si falló
        """
        try:
            # Crear directorio si no existe
            os.makedirs(self.base_path, exist_ok=True)
            
            # Descargar imagen
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            
            # Guardar archivo
            file_path = os.path.join(self.base_path, filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)
            
            print(f"Imagen descargada: {filename}")
            return filename
            
        except Exception as e:
            print(f"Error descargando imagen {filename}: {e}")
            return None
    
    def download_question_image(self, question_element, question_id: str) -> Optional[str]:
        """
        Descarga la imagen de una pregunta si existe.
        
        Args:
            question_element: Elemento web de la pregunta
            question_id: ID de la pregunta
            
        Returns:
            Ruta del archivo guardado o None si no hay imagen
        """
        try:
            # Buscar imagen en la pregunta
            img_element = question_element.find_element(By.CSS_SELECTOR, "img")
            img_src = img_element.get_attribute("src")
            
            if img_src:
                # Extraer extensión de la URL
                extension = self._get_extension_from_url(img_src)
                filename = f"pregunta_{question_id}{extension}"
                return self.download_image(img_src, filename)
            
            return None
            
        except Exception:
            # No hay imagen en la pregunta
            return None
    
    def download_option_images(self, option_elements, question_id: str) -> List[Optional[str]]:
        """
        Descarga las imágenes de las opciones de una pregunta.
        
        Args:
            option_elements: Elementos web de las opciones
            question_id: ID de la pregunta
            
        Returns:
            Lista de rutas de archivos guardados
        """
        image_paths = []
        
        for i, option_element in enumerate(option_elements):
            try:
                # Buscar imagen en la opción
                img_element = option_element.find_element(By.CSS_SELECTOR, "img")
                img_src = img_element.get_attribute("src")
                
                if img_src:
                    extension = self._get_extension_from_url(img_src)
                    filename = f"pregunta_{question_id}_opcion_{i+1}{extension}"
                    downloaded_path = self.download_image(img_src, filename)
                    image_paths.append(downloaded_path)
                else:
                    image_paths.append(None)
                    
            except Exception:
                # No hay imagen en esta opción
                image_paths.append(None)
        
        return image_paths
    
    def _get_extension_from_url(self, url: str) -> str:
        """
        Extrae la extensión del archivo desde una URL.
        
        Args:
            url: URL del archivo
            
        Returns:
            Extensión del archivo (incluyendo el punto)
        """
        try:
            # Obtener la extensión desde la URL
            path = url.split('?')[0]  # Remover parámetros de consulta
            extension = os.path.splitext(path)[1]
            
            # Extensiones válidas para imágenes
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
            
            if extension.lower() in valid_extensions:
                return extension
            else:
                return '.png'  # Por defecto
                
        except Exception:
            return '.png'  # Por defecto