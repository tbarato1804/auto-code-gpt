
# send_to_openai.py
import openai
import json
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

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

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un experto en Python que ayuda a depurar scripts de automatización."},
            {"role": "user", "content": prompt}
        ]
    )

    suggestion = response.choices[0].message["content"]
    with open("suggestion.txt", "w") as f:
        f.write(suggestion)

    print("✍️ Sugerencia guardada en suggestion.txt")

if __name__ == "__main__":
    main()
