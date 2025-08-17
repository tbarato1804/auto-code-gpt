import os
import subprocess
from openai import OpenAI

REPO_URL = "https://github.com/tbarato1804/tradier-bot.git"
CLONE_DIR = "temp_tradier_bot"
FILES_TO_ANALYZE = ["main.py", "order.py", "config.py", "trading/logic.py"]

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_file(file_path):
    with open(file_path, "r") as f:
        content = f.read()
    prompt = f"""
    Eres un experto en trading y programación Python.
    Analiza este archivo de un bot de trading y sugiere mejoras estructurales, de claridad, seguridad y eficiencia.
    Devuelve solo el nuevo código con las mejoras aplicadas, sin explicaciones.
    Código:
    ```python
    {content}
    ```
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Eres un programador experto en bots financieros."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    subprocess.run(["git", "clone", REPO_URL, CLONE_DIR], check=True)
    os.makedirs("improvements", exist_ok=True)
    for file in FILES_TO_ANALYZE:
        full_path = os.path.join(CLONE_DIR, file)
        if os.path.exists(full_path):
            suggestion = analyze_file(full_path)
            out_path = os.path.join("improvements", f"improvement_{os.path.basename(file)}.txt")
            with open(out_path, "w") as out_file:
                out_file.write(suggestion)
                print(f"✅ Mejora generada para {file} → {out_path}")
        else:
            print(f"❌ Archivo no encontrado: {file}")

if __name__ == "__main__":
    main()
