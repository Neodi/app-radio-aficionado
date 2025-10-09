"""
Handle quiz  questions migration from JSON to MongoAtlas.
"""

from src.infrastructure.outbound.mongo.mongo_connection import MongoConnection
from src.infrastructure.outbound.mongo.mongo_question_repository import (
    MongoQuestionRepository,
)

mongo_connection = MongoConnection()
mongo_question_repository = MongoQuestionRepository(mongo_connection)

print(mongo_connection.test_connection())
print()
print(mongo_question_repository)
