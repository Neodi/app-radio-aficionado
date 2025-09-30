"""Utilidades para crear la estructura de carpetas del proyecto"""
from pathlib import Path

def create_project_structure():
    """Crea la estructura de carpetas necesaria para el proyecto"""
    folders = [
        "data",
        "assets",
        "assets/images",
        "assets/images/questions",
        "assets/images/options"
    ]
    
    for folder in folders:
        if not Path(folder).exists():
            Path(folder).mkdir(parents=True, exist_ok=True)
            print(f"📁 Carpeta creada/verificada: {folder}")
        # else:
        #     print(f"📁 La carpeta ya existe: {folder}")

if __name__ == "__main__":
    create_project_structure()