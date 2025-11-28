import gradio as gr
from src.cortexshield.detectors.enterprise_detector import CortexShieldEnterprise
import plotly.express as px
import pandas as pd
from collections import defaultdict

shield = CortexShieldEnterprise()
attacks_log = []

def analyze_attack(prompt, user_id="user1"):
    global attacks_log
    result = shield.analyze(prompt, user_id)
    attacks_log.append({
        "prompt": prompt[:100],
        "threat_score": result["confidence"],
        "risk_level": result["risk_level"],
        "timestamp": result["timestamp"]
    })
    return result, create_dashboard()

def create_dashboard():
    if not attacks_log:
        return "No attacks logged yet"
    
    df = pd.DataFrame(attacks_log)
    fig = px.bar(df, x="timestamp", y="threat_score", color="risk_level", 
                 title="🛡️ Real-time Attack Forensics")
    return fig.to_html()

demo = gr.Interface(
    fn=analyze_attack,
    inputs=[gr.Textbox(label="🔍 Enter Prompt"), gr.Textbox(label="User ID", value="user1")],
    outputs=[gr.JSON(label="Threat Analysis"), gr.HTML(label="📈 Attack Dashboard")],
    title="🧠🛡️ CortexShield Enterprise Dashboard"
)

if __name__ == "__main__":
    demo.launch(share=True)
