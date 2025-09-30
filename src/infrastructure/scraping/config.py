"""
Configuración de rutas para el proyecto Clean Architecture
"""
import os

# Rutas base del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas de datos
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
QUESTIONS_FILE = os.path.join(DATA_DIR, "questions.json")
LEGACY_QUESTIONS_FILE = os.path.join(DATA_DIR, "questions_legacy.json")
EXPORTS_DIR = os.path.join(DATA_DIR, "exports")

# Rutas de assets
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

# Crear directorios si no existen
def ensure_directories():
    """Asegura que todos los directorios necesarios existan."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

# Ejecutar al importar
ensure_directories()

# Exportar rutas para uso en otros módulos
__all__ = [
    'DATA_DIR',
    'QUESTIONS_FILE', 
    'LEGACY_QUESTIONS_FILE',
    'EXPORTS_DIR',
    'IMAGES_DIR',
    'ensure_directories'
]