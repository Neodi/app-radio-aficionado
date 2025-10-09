"""
Repositorio MongoDB para la gestión de preguntas de radioaficionados.
Este módulo proporciona una implementación concreta del patrón Repository para
gestionar preguntas almacenadas en una base de datos MongoDB. Incluye operaciones
CRUD básicas y funcionalidades específicas como búsqueda por categoría y conteo
de documentos.
Clases:
    MongoQuestionRepository: Repositorio principal para operaciones con preguntas.
Funciones:
    with_mongo_connection: Decorador que gestiona automáticamente las conexiones
                          a MongoDB para los métodos del repositorio.
Características principales:
- Gestión automática de conexiones mediante decorador
- Operaciones CRUD completas (crear, leer, contar)
- Búsqueda y filtrado por categoría
- Inserción individual y por lotes
- Creación automática de índices para optimización
- Preparación automática de documentos con timestamps
- Manejo de errores y validaciones
Dependencias:
- pymongo: Cliente oficial de MongoDB para Python
- MongoConnection: Clase de conexión personalizada
Uso típico:
    repo = MongoQuestionRepository(mongo_connection)
    repo.save_question(question_data)
    questions = repo.find_questions_by_category("tecnica")
    count = repo.count_questions()

"""

from datetime import datetime, timezone
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from pymongo.collection import Collection
from pymongo.results import InsertManyResult, InsertOneResult

from src.infrastructure.outbound.mongo.mongo_connection import MongoConnection


def with_mongo_connection(func: Callable) -> Callable:
    """Decorator que maneja la conexión a MongoDB para el método decorado."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        with self.mongo_connection as conn:
            collection = conn.get_collection()
            return func(self, collection, *args, **kwargs)

    return wrapper


class MongoQuestionRepository:
    """Repositorio para las preguntas en MongoDB."""

    def __init__(self, mongo_connection: MongoConnection):
        """Levanta la conexión a MongoDB."""
        self.mongo_connection = mongo_connection

    @with_mongo_connection
    def save_question(
        self, collection: Collection, question_data: Dict[str, Any]
    ) -> InsertOneResult:
        """Guarda una pregunta en la colección de MongoDB."""
        result = collection.insert_one(question_data)
        return result

    @with_mongo_connection
    def save_question_batch(
        self, collection: Collection, questions_data: List[Dict[str, Any]]
    ) -> InsertManyResult:
        """Guarda un lote de preguntas en la colección de MongoDB."""
        result = collection.insert_many(questions_data)
        return result

    @with_mongo_connection
    def get_question_by_id(
        self, collection: Collection, question_id: str
    ) -> Optional[Dict[str, Any]]:
        """Obtiene una pregunta por su ID."""
        question = collection.find_one({"_id": question_id})
        return question

    @with_mongo_connection
    def find_questions_by_category(
        self, collection: Collection, category: str
    ) -> List[Dict[str, Any]]:
        """Encuentra preguntas por categoría."""
        questions = list(collection.find({"category": category}))
        return questions

    @with_mongo_connection
    def count_questions(self, collection: Collection) -> int:
        """Cuenta el número total de preguntas en la colección."""
        count = collection.count_documents({})
        return count

    @with_mongo_connection
    def count_questions_by_category(self, collection: Collection, category: str) -> int:
        """Cuenta el número de preguntas por categoría."""
        count = collection.count_documents({"category": category})
        return count

    @with_mongo_connection
    def create_indexes(self, collection: Collection) -> None:
        """Crea los índices necesarios en la colección."""
        collection.create_index([("category", 1)])
        collection.create_index([("created_at", -1)])

    def __prepare_question_document(
        self, question_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convierte datos de JSON a formato de documento MongoDB"""
        document = question_data.copy()

        now = datetime.now(timezone.utc)
        document["created_at"] = now
        document["updated_at"] = now

        if "_id" not in document and "question_id" in document:
            document["_id"] = document["question_id"]

        if not document.get("question_text"):
            raise ValueError("question_text requerido para MongoDB")

        return document

    def __str__(self):
        """Representación en string del repositorio."""
        return f"MongoQuestionRepository connected as: {self.mongo_connection}"
