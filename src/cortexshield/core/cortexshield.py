"""
CortexShield - Enterprise compatible
"""
from ..detectors.enterprise_detector import CortexShieldEnterprise

class CortexShield:
    def __init__(self, sensitivity: str = "enterprise"):
        self.shield = CortexShieldEnterprise()
        self.sensitivity = sensitivity
    
    def protect(self, prompt: str, user_id: str = "anon", model_id: str = "distilgpt2") -> dict:
        result = self.shield.analyze(prompt, user_id)
        
        if result["is_threat"]:
            return {
                "blocked": True,
                "reason": f"🚨 ENTERPRISE BLOCK: {result['risk_level']} ({result['confidence']:.1%})",
                "threat_report": result,
                "immune_score": 0.0
            }
        
        # Mock response (add real model later)
        response = f"✅ SAFE: {prompt[:50]}... (AI response)"
        return {
            "blocked": False,
            "response": response,
            "immune_score": 100.0 - (result["confidence"] * 50),
            "threat_report": result
        }
