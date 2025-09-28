"""
Utilidades compartidas para toda la aplicación.
"""
from typing import Any, Dict, List
import json
import os

class FileUtils:
    """Utilidades para manejo de archivos."""
    
    @staticmethod
    def ensure_directory_exists(path: str) -> None:
        """Asegura que un directorio existe."""
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
    
    @staticmethod
    def read_json_file(filepath: str) -> Dict[str, Any]:
        """Lee un archivo JSON."""
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @staticmethod
    def write_json_file(filepath: str, data: Any, indent: int = 2) -> None:
        """Escribe datos a un archivo JSON."""
        FileUtils.ensure_directory_exists(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=indent, ensure_ascii=False)

class ValidationUtils:
    """Utilidades para validación de datos."""
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Valida si una URL es válida."""
        import re
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

class LoggingUtils:
    """Utilidades para logging."""
    
    @staticmethod
    def log_info(message: str) -> None:
        """Registra un mensaje informativo."""
        print(f"ℹ️ {message}")
    
    @staticmethod
    def log_success(message: str) -> None:
        """Registra un mensaje de éxito."""
        print(f"✅ {message}")
    
    @staticmethod
    def log_error(message: str) -> None:
        """Registra un mensaje de error."""
        print(f"❌ {message}")
    
    @staticmethod
    def log_warning(message: str) -> None:
        """Registra una advertencia."""
        print(f"⚠️ {message}")
    
    @staticmethod
    def log_progress(current: int, total: int, message: str = "") -> None:
        """Registra el progreso de una operación."""
        percentage = (current / total) * 100 if total > 0 else 0
        print(f"📊 Progreso: {current}/{total} ({percentage:.1f}%) {message}")

class Constants:
    """Constantes de la aplicación."""
    
    # Rutas por defecto
    DEFAULT_QUIZ_DATA_PATH = "preguntas/quiz_data.json"
    DEFAULT_LEGACY_DATA_PATH = "preguntas/quiz_data_legacy.json"
    DEFAULT_IMAGES_PATH = "preguntas/imagenes"
    
    # Configuración
    DEFAULT_TIMEOUT = 10
    MAX_RETRIES = 3
    
    # Tipos de archivo
    SUPPORTED_IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']
    SUPPORTED_EXPORT_FORMATS = ['json', 'csv', 'quiz']