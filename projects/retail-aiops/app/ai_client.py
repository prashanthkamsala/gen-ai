import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, OpenAIError

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_incident_with_ai(incident: dict) -> dict:
    try:
        prompt = f"""
You are a senior Site Reliability Engineer for a large retail platform.

Analyze the following incident and provide:
1. A short incident summary
2. The most likely root cause
3. 3 clear remediation steps

Incident details:
Service: {incident['service']}
Severity: {incident['severity']}
Metrics: {incident['metrics']}
Logs: {incident['logs']}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert SRE and AIOps analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return {
            "analysis": response.choices[0].message.content
        }

    except RateLimitError:
        # REAL-WORLD fallback
        return {
            "analysis": "AI analysis is temporarily unavailable due to quota limits.",
            "note": "This system is designed to gracefully handle AI service rate limits."
        }

    except OpenAIError as e:
        return {
            "analysis": "AI service error occurred.",
            "error": str(e)
        }
