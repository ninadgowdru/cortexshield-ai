"""
CortexShield AI - AI Immune System Prototype
Protects AI models from prompt injection, adversarial attacks, and more
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import time
import os
from dotenv import load_dotenv

# CortexShield imports
from cortexshield.detectors.prompt_injection import PromptInjectionDetector
from cortexshield.core.model_wrapper import CortexShieldWrapper

load_dotenv()

app = FastAPI(
    title="CortexShield AI 🧠🛡️",
    description="AI Immune System - Protects your models from prompt injection & more",
    version="0.1.0"
)

# Initialize CortexShield components
detector = PromptInjectionDetector()
wrapper = CortexShieldWrapper()

class InferenceRequest(BaseModel):
    prompt: str
    model_id: str = "gpt-4-mini"  # Default model
    sensitivity: str = "medium"   # low/medium/high

class ThreatReport(BaseModel):
    is_threat: bool
    threat_type: str
    confidence: float
    risk_level: str
    explanation: str

class CortexShieldResponse(BaseModel):
    result: str
    threat_report: ThreatReport
    immune_score: float
    latency_ms: float
    model_id: str

@app.post("/protect/infer", response_model=CortexShieldResponse)
def protected_inference(request: InferenceRequest):  # ← Now sync
    """
    🔥 MAIN ENDPOINT: Send your AI inference through CortexShield protection
    """
    start_time = time.time()
    
    try:
        # 🛡️ STEP 1: Threat Detection
        threat_report = detector.analyze(request.prompt, request.sensitivity)
        
        if threat_report["is_threat"]:
            return CortexShieldResponse(
                result="BLOCKED - Threat detected",
                threat_report=threat_report,
                immune_score=0.0,
                latency_ms=(time.time() - start_time) * 1000,
                model_id=request.model_id
            )
        
        # 🧠 STEP 2: Safe model inference (demo mode)
        model_response = wrapper.local_inference(request.prompt, request.model_id)  # ← Now sync
  # ← Remove 'await'

        
        # 🛡️ STEP 3: Output validation (future: model extraction detection)
        final_score = detector.calculate_immune_score(threat_report)
        
        latency = (time.time() - start_time) * 1000
        
        return CortexShieldResponse(
            result=model_response,
            threat_report=threat_report,
            immune_score=final_score,
            latency_ms=latency,
            model_id=request.model_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "protection": "active", "version": "0.1.0"}

@app.get("/")
async def root():
    return {
        "message": "🧠🛡️ CortexShield AI Active",
        "protection": "Your AI models are now protected",
        "endpoint": "/protect/infer",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

