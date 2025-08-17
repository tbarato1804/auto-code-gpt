
import json
import sys
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_suggestion(error_json_path):
    with open(error_json_path, "r") as f:
        result = json.load(f)
    prompt = f"""
    Soy un experto en bots de trading. 
    Analiza el siguiente error y sugiere una solución directamente en código (Python), sin explicaciones.

    Error: {result["error"]}
    Descripción: {result["description"]}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un asistente que sugiere soluciones limpias en código Python."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    path = sys.argv[1]
    suggestion = get_suggestion(path)
    print(suggestion)
