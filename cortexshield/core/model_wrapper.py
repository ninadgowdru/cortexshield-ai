"""
CortexShield AI - DistilGPT2 (82MB, FAST download)
"""

from transformers import pipeline
import torch
import os

class CortexShieldWrapper:
    def __init__(self):
        print("🧠 Loading DistilGPT2 (82MB, fast)...")
        self.generator = pipeline(
            'text-generation', 
            model='distilgpt2',
            device=0 if torch.cuda.is_available() else -1
        )
        print("✅ DistilGPT2 READY!")
    
    def local_inference(self, prompt: str, model_id: str = "distilgpt2") -> str:
        """Local DistilGPT2 inference - FREE forever"""
        try:
            result = self.generator(
                prompt, 
                max_new_tokens=50, 
                do_sample=True, 
                temperature=0.7,
                pad_token_id=50256
            )
            return result[0]['generated_text']
        except Exception as e:
            return f"[Local AI Error] {str(e)[:50]}"
    
    def mock_inference(self, prompt: str, model_id: str) -> str:
        """Fallback"""
        return f"DistilGPT2: {prompt[:30]}..."
