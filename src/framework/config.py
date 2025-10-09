"""
Módulo de configuración para la aplicación de radioaficionado.
Este módulo proporciona una clase de configuración centralizada que carga variables
de entorno para varios componentes de la aplicación, incluyendo objetivos de web scraping
y conexiones a la base de datos MongoDB.
La configuración se carga desde variables de entorno usando python-dotenv,
permitiendo un despliegue flexible en diferentes entornos.
Clases:
    Config: Clase principal de configuración que contiene todas las configuraciones de la aplicación.
Variables de Entorno Requeridas:
    - URL_RADIOELECTRICIDAD: URL para el objetivo de scraping de radioelectricidad
    - CATEGORY_RADIOELECTRICIDAD: Categoría para el contenido de radioelectricidad
    - URL_NORMATIVA: URL para el objetivo de scraping de normativa
    - CATEGORY_NORMATIVA: Categoría para el contenido de normativa
    - MONGODB_USERNAME: Nombre de usuario para autenticación en MongoDB
    - MONGODB_PASSWORD: Contraseña para autenticación en MongoDB
    - MONGODB_URI: URI de conexión a MongoDB
    - MONGODB_DATABASE_NAME: Nombre de la base de datos MongoDB
    - MONGODB_COLLECTION_NAME: Nombre de la colección MongoDB
    - MY_IP: Dirección IP para configuración de red
Ejemplo:
    # Acceder a valores de configuración
    db_uri = Config.MONGODB_URI
    scraping_url = Config.URL_RADIOELECTRICIDAD

"""

import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for the application."""

    # =================================
    # SCRAPING
    # =================================
    URL_RADIOELECTRICIDAD = os.getenv("URL_RADIOELECTRICIDAD")
    CATEGORY_RADIOELECTRICIDAD = os.getenv("CATEGORY_RADIOELECTRICIDAD")

    URL_NORMATIVA = os.getenv("URL_NORMATIVA")
    CATEGORY_NORMATIVA = os.getenv("CATEGORY_NORMATIVA")

    # =================================
    # MONGODB
    # =================================
    MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")
    MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")

    MONGODB_URI = os.getenv("MONGODB_URI")

    MONGODB_DATABASE_NAME = os.getenv("MONGODB_DATABASE_NAME")
    MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME")

    MY_IP = os.getenv("MY_IP")
