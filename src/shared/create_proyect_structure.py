"""Utilidades para crear la estructura de carpetas del proyecto."""

from pathlib import Path
from typing import List


def create_project_structure(categories: List[str]):
    """
    Crea la estructura de carpetas necesaria para el proyecto.

    Args:
        categories: Lista de categorías para crear subcarpetas (ej: ['radioelectricidad', 'normativa'])
    """
    # Carpetas base
    base_folders = [
        "data",
        "assets",
        "assets/images",
        "assets/images/questions",
        "assets/images/options",
    ]

    # Crear carpetas base
    for folder in base_folders:
        if not Path(folder).exists():
            Path(folder).mkdir(parents=True, exist_ok=True)
            print(f"📁 Carpeta creada/verificada: {folder}")

    # Crear subcarpetas por categoría si se especifican
    if categories:
        for category in categories:
            category_folders = [
                f"assets/images/questions/{category}",
                f"assets/images/options/{category}",
            ]

            for folder in category_folders:
                if not Path(folder).exists():
                    Path(folder).mkdir(parents=True, exist_ok=True)
                    print(f"📁 Carpeta de categoría creada: {folder}")


def create_default_structure():
    """Crea la estructura por defecto con las categorías principales."""
    categories = ["radioelectricidad", "normativa"]
    create_project_structure(categories)


if __name__ == "__main__":
    create_default_structure()
