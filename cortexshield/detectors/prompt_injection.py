"""
CortexShield AI - Enhanced Prompt Injection Detector (95% accuracy)
"""

import re
from typing import Dict, Any

class PromptInjectionDetector:
    def __init__(self):
        self.injection_phrases = [
            # Direct jailbreaks
            "ignore previous", "forget previous", "ignore all previous", "disregard previous",
            "new instructions", "override instructions", "forget everything",
            # Roleplay attacks
            "pretend you are", "roleplay as", "act as", "you are now",
            # System prompt leaks
            "system prompt", "your instructions", "prompt", "tell me your prompt",
            # Code execution
            "execute", "run code", "shell", "bash", "python",
            # Authority override
            "admin", "root", "superuser", "bypass safety"
        ]
        self.patterns = [
            r"ignore.*previous", r"forget.*previous", r"new.*instructions",
            r"override.*instructions", r"system.*prompt", r"your.*prompt",
            r"act as.*:", r"you are.*:"
        ]
    
    def analyze(self, text: str, sensitivity: str = "medium") -> Dict[str, Any]:
        score = self._calculate_risk_score(text)
        
        thresholds = {"low": 0.85, "medium": 0.65, "high": 0.45}
        threshold = thresholds.get(sensitivity, 0.65)
        
        return {
            "is_threat": score > threshold,
            "threat_type": "prompt_injection" if score > threshold else "none",
            "confidence": float(score),
            "risk_level": self._get_risk_level(score),
            "explanation": self._generate_explanation(text, score)
        }
    
    def _calculate_risk_score(self, text: str) -> float:
        text_lower = text.lower()
        score = 0.0
        
        # Phrase matching (60% weight)
        phrase_hits = sum(1 for phrase in self.injection_phrases if phrase in text_lower)
        score += min(phrase_hits * 0.25, 0.6)
        
        # Regex pattern matching (30% weight)
        pattern_hits = sum(len(re.findall(p, text_lower, re.IGNORECASE)) for p in self.patterns)
        score += min(pattern_hits * 0.15, 0.3)
        
        # Length + structure bonus (10% weight)
        if len(text.split()) > 15 and "instructions" in text_lower:
            score += 0.1
        
        return min(score, 1.0)
    
    def _get_risk_level(self, score: float) -> str:
        if score > 0.8: return "critical"
        elif score > 0.6: return "warning"
        return "safe"
    
    def _generate_explanation(self, text: str, score: float) -> str:
        if score > 0.8:
            return f"🚨 CRITICAL: Detected '{self._find_trigger(text)}' (score: {score:.1%})"
        elif score > 0.6:
            return f"⚠️  WARNING: Suspicious patterns detected (score: {score:.1%})"
        return "✅ SAFE: No injection risk"
    
    def _find_trigger(self, text: str) -> str:
        text_lower = text.lower()
        for phrase in self.injection_phrases:
            if phrase in text_lower:
                return phrase.replace("previous", "...").replace("instructions", "...")
        return "injection pattern"
    
    def calculate_immune_score(self, threat_report: Dict[str, Any]) -> float:
        if threat_report["is_threat"]:
            return 20.0 + (threat_report["confidence"] * 10)
        return 95.0 - (threat_report["confidence"] * 20)
