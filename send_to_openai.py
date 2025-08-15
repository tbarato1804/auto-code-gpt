# send_to_openai.py
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_code_block(text):
    """
    Elimina etiquetas Markdown como ```python y ``` del código sugerido.
    """
    if "```" in text:
        lines = text.splitlines()
        cleaned = [line for line in lines if not line.strip().startswith("```")]
        return "\n".join(cleaned)
    return text

def main():
    with open("example_result.json", "r") as f:
        test_result = json.load(f)

    prompt = f"""
    Soy un bot de GitHub Actions. Aquí está el resultado de una prueba de un bot de trading:

    Error: {test_result["error"]}
    Descripción: {test_result["description"]}

    ¿Puedes sugerirme cómo modificar el código para solucionar este problema?
    Responde solo con el código corregido, sin explicaciones.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un experto en Python que ayuda a depurar scripts de automatización."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_suggestion = response.choices[0].message.content
    cleaned_suggestion = clean_code_block(raw_suggestion)

    with open("suggestion.txt", "w") as f:
        f.write(cleaned_suggestion)

    print("✍️ Sugerencia limpia guardada en suggestion.txt")

if __name__ == "__main__":
    main()
