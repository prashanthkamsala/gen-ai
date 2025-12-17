from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from app.ai_client import analyze_incident_with_ai

app = FastAPI(title="Retail AIOps Assistant")

class IncidentRequest(BaseModel):
    service: str
    severity: str
    metrics: Dict[str, str]
    logs: List[str]

@app.post("/analyze-incident")
def analyze_incident(incident: IncidentRequest):
    ai_result = analyze_incident_with_ai(incident.dict())
    return ai_result
