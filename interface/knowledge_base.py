from pyswip import Prolog
from config import KB_PATH


class KnowledgeBase:

    def __init__(self):
        self.prolog = Prolog()
        kb = KB_PATH.replace("\\", "/")
        self.prolog.consult(kb)

    def get_diseases(self, crop: str) -> list[str]:
      
        results = list(self.prolog.query(f"get_all_diseases({crop}, Diseases)"))
        if not results:
            return []
        return [str(d) for d in results[0]["Diseases"]]

    def get_disease_info(self, crop: str, disease: str) -> dict:
       
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
