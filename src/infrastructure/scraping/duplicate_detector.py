"""Servicio para detectar preguntas duplicadas"""

import json
import os
from typing import Dict, List, Set

from ...domain.quiz.quiz_question_model import QuizQuestionModel


class DuplicateDetector:
    """Detecta preguntas duplicadas usando fingerprints"""

    def __init__(self, data_path: str = "data/questions.json"):
        """Inicializa el detector con la ruta al archivo de datos existente."""
        self.data_path = data_path
        self.existing_fingerprints: Set[str] = set()
        self._load_existing_fingerprints()

    def _load_existing_fingerprints(self):
        """Carga los fingerprints de las preguntas existentes"""
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
                    print(
                        f"🔍 Cargando {len(existing_data)} preguntas existentes para detectar duplicados..."
                    )
                    for item in existing_data:
                        try:
                            question = QuizQuestionModel(**item)
                            self.existing_fingerprints.add(question.fingerprint)
                        except Exception as e:
                            print(f"⚠️ Error procesando pregunta existente: {e}")
            except Exception as e:
                print(f"⚠️ Error cargando fingerprints existentes: {e}")
        else:
            print("📁 Archivo de preguntas no existe, iniciando con lista vacía")

    def filter_duplicates(
        self, new_questions: List[QuizQuestionModel]
    ) -> List[QuizQuestionModel]:
        """Filtra preguntas duplicadas de una lista nueva"""
        unique_questions = []
        session_fingerprints = set()

        duplicates_vs_existing = 0
        duplicates_in_session = 0

        for question in new_questions:
            fingerprint = question.fingerprint

            # Verificar duplicado vs preguntas existentes
            if fingerprint in self.existing_fingerprints:
                duplicates_vs_existing += 1
                print(f"🔄 Duplicado vs existentes: {question.title.titleText[:50]}...")
                continue

            # Verificar duplicado en la sesión actual
            if fingerprint in session_fingerprints:
                duplicates_in_session += 1
                print(f"🔄 Duplicado en sesión: {question.title.titleText[:50]}...")
                continue

            # La pregunta es única
            unique_questions.append(question)
            session_fingerprints.add(fingerprint)

        return unique_questions

    def get_duplicate_report(self, questions: List[QuizQuestionModel]) -> Dict:
        """Genera un reporte de duplicados."""
        fingerprints = [q.fingerprint for q in questions]
        unique_fingerprints = set(fingerprints)

        return {
            "total_questions": len(questions),
            "unique_questions": len(unique_fingerprints),
            "duplicates_found": len(questions) - len(unique_fingerprints),
            "existing_questions": len(self.existing_fingerprints),
        }
