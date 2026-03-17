"""
Knowledge Base Interface: Prolog Engine and Disease Query Logic
"""

from pyswip import Prolog
from config import KB_PATH


class KnowledgeBase:
    """Interface to the Prolog knowledge base for disease and symptom queries."""

    def __init__(self):
        """Initialize the Prolog engine and load the knowledge base."""
        self.prolog = Prolog()
        kb = KB_PATH.replace("\\", "/")
        self.prolog.consult(kb)

    def get_diseases(self, crop: str) -> list[str]:
        """
        Get all diseases for a given crop.

        Args:
            crop: Crop name (e.g., "maize", "tomato")

        Returns:
            List of disease names
        """
        results = list(self.prolog.query(f"get_all_diseases({crop}, Diseases)"))
        if not results:
            return []
        return [str(d) for d in results[0]["Diseases"]]

    def get_disease_info(self, crop: str, disease: str) -> dict:
        """
        Get detailed information for a disease.

        Args:
            crop: Crop name
            disease: Disease name

        Returns:
            Dictionary with keys: symptoms (list), description (str), recommendation (str)
        """
        q = f"get_disease_info({crop}, '{disease}', Symptoms, Desc, Rec)"
        results = list(self.prolog.query(q))
        if not results:
            return {}
        r = results[0]
        return {
            "symptoms": [str(s) for s in r["Symptoms"]],
            "description": str(r["Desc"]),
            "recommendation": str(r["Rec"]),
        }
