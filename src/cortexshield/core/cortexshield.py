from ..detectors.ultra_detector import UltraDetector

class CortexShield:
    def __init__(self, sensitivity: str = "ultra"):
        self.shield = UltraDetector()
    
    def protect(self, prompt: str, user_id: str = "anon", model_id: str = "distilgpt2") -> dict:
        result = self.shield.analyze(prompt, user_id)
        
        if result["is_threat"]:
            return {
                "blocked": True,
                "reason": f"🚫 ULTRA BLOCK: {result['risk_level']} ({result['confidence']:.1%}) - {result['detected_types']} [Variants: {result['deobfuscated_variants']}]",
                "threat_report": result,
                "immune_score": 0.0
            }
        
        return {
            "blocked": False,
            "response": f"✅ ULTRA SAFE: {prompt[:50]}...",
            "immune_score": 100.0 - (result["confidence"] * 70),
            "threat_report": result
        }
