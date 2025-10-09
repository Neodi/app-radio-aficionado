"""
Módulo para manejar conexiones a MongoDB Atlas.
Este módulo proporciona una clase MongoConnection que actúa como un administrador
de contexto para establecer y gestionar conexiones a MongoDB Atlas de forma segura.
Classes:
    MongoConnection: Administrador de contexto para conexiones MongoDB Atlas.
Example:
    >>> with MongoConnection() as conn:
    ...     db = conn.get_database()
    ...     collection = conn.get_collection()
    ...     # Realizar operaciones con la base de datos

"""

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from src.framework.config import Config


class MongoConnection:
    """Clase para manejar la conexión a MongoDB Atlas con context manager."""

    def __init__(self, mongo_collection: str | None = Config.MONGODB_COLLECTION_NAME):
        """Inicializa la configuración de la conexión con las variables de entorno."""
        self.uri = Config.MONGODB_URI
        self.client = None
        self.db = Config.MONGODB_DATABASE_NAME or "not_.env_db"
        self.collection = mongo_collection or "not_.env_collection"

    def connect(self):
        """Establece la conexión a MongoDB Atlas."""
        self.client = MongoClient(self.uri)

        return self.client

    def disconnect(self):
        """Cierra la conexión a MongoDB Atlas."""
        if self.client:
            self.client.close()
        else:
            raise ConnectionError("No hay una conexión activa para cerrar.")

    def get_database(self) -> Database:
        """Devuelve la base de datos conectada."""
        if self.client:
            return self.client[self.db]
        else:
            raise ConnectionError("No hay una conexión activa.")

    def get_collection(self) -> Collection:
        """Devuelve la colección conectada."""
        if self.client:
            return self.client[self.db][self.collection]
        else:
            raise ConnectionError("No hay una conexión activa.")

    def __enter__(self):
        """Método para entrar en el contexto del administrador de contexto."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Método para salir del contexto del administrador de contexto."""
        self.disconnect()

    def test_connection(self) -> bool:
        """Prueba la conexión a MongoDB Atlas."""
        try:
            with self:
                if self.client:
                    self.client.admin.command("ping")
                    return True
                return False
        except Exception:
            return False

    def __str__(self):
        """
        Devuelve una representación en cadena de la conexión a MongoDB.
        """
        return (
            "MongoConnection_settings(\n"
            f"  uri='{self.uri}',\n"
            f"  db='{self.db}',\n"
            f"  collection='{self.collection}'\n"
            ")"
        )
