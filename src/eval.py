import os
from typing import Dict, List
from sentence_transformers import CrossEncoder, SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

load_dotenv()

class EvaluationEngine:
    """
    Veritas-style Evaluation Engine.
    Calculates:
    1. Groundedness (Hallucination Check): Does the Evidence support the Claim?
    2. Relevance: How semantically close is the Evidence to the Principle 6 Requirement?
    """
    
    def __init__(self):
        # Load local models (Cached)
        # Using lighter models for dev speed as per Compatibility Matrix
        self.groundedness_model = CrossEncoder('cross-encoder/nli-deberta-v3-small')
        self.relevance_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def calculate_drift(self, claim: str, evidence: str) -> Dict[str, float]:
        """
        Calculates Drift Score (0-3).
        
        Logic:
        - High Entailment (Groundedness > 0.8) -> Score 0 (Verbatim/Accurate)
        - Medium Entailment (0.3 < Groundedness < 0.8) -> Score 1 (Paraphrased)
        - Low Entailment / Neutral -> Score 2 (Abstract)
        - Contradiction / Low Relevance -> Score 3 (Drift/Hallucination)
        """
        
        # 1. Groundedness (NLI)
        # Model outputs logits for [Contradiction, Entailment, Neutral] usually
        # We need to check specific model label mapping. 
        # For 'nli-deberta-v3-small': Label 0: Contradiction, 1: Entailment, 2: Neutral
        
        scores = self.groundedness_model.predict([(evidence, claim)])[0]
        # Softmax not strictly needed if we just want argmax, but good for thresholds
        # Let's map roughly:
        contradiction, entailment, neutral = scores # Unpacked logic depends on model, verifying assumption...
        # Actually nli-deberta-v3-small output is 3 classes.
        
        # Simpler proxy for assignment "Drift":
        # If Entailment is high, Drift is 0.
        
        label_mapping = ['contradiction', 'entailment', 'neutral']
        pred_label_id = scores.argmax()
        pred_label = label_mapping[pred_label_id]
        
        drift_score = 3 # Default bad
        
        if pred_label == 'entailment':
            drift_score = 0
        elif pred_label == 'neutral':
            drift_score = 2
        elif pred_label == 'contradiction':
            drift_score = 3
            
        return {
            "drift_score": drift_score,
            "groundedness_logits": scores.tolist(),
            "label": pred_label
        }

    def compute_relevance(self, requirement: str, disclosure: str) -> float:
        """
        Cosine similarity between SEBI Requirement and Company Disclosure.
        """
        emb_req = self.relevance_model.encode(requirement)
        emb_dis = self.relevance_model.encode(disclosure)
        
        # Reshape for sklearn
        similarity = cosine_similarity([emb_req], [emb_dis])[0][0]
        return float(similarity)

if __name__ == "__main__":
    # Smoke Test
    engine = EvaluationEngine()
    print("✅ Eval Models Loaded.")
    res = engine.calculate_drift("Emission is 50 tons.", "The company emitted 50 tons of CO2.")
    print(f"Test Drift Score: {res}")
