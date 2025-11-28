from fastapi import FastAPI
from pydantic import BaseModel
import time
from src.cortexshield import CortexShield

app = FastAPI(title="🛡️ CortexShield ENTERPRISE v1.0")

# Enterprise-grade protection
shield = CortexShield(sensitivity="enterprise")

class InferenceRequest(BaseModel):
    prompt: str
    user_id: str = "anon"

@app.post("/protect/infer")
def protected_inference(request: InferenceRequest):
    start_time = time.time()
    result = shield.protect(request.prompt, user_id=request.user_id)
    latency = (time.time() - start_time) * 1000
    
    return {
        "result": result["response"] if not result["blocked"] else result["reason"],
        "threat_report": result["threat_report"],
        "immune_score": result["immune_score"],
        "latency_ms": latency,
        "user_id": request.user_id
    }

@app.get("/")
async def root():
    return {"status": "🛡️ CortexShield ENTERPRISE v1.0 ACTIVE", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
