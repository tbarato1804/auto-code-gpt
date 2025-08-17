
import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Recopilar el contenido de todos los archivos .py (excepto tests)
code_to_analyze = ""
for root, _, files in os.walk("tradier"):
    for file in files:
        if file.endswith(".py") and not file.startswith("test_"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                code_to_analyze += f"

# === Archivo: " + path + " ===
" + f.read()

# Solicitar sugerencias explicadas a OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Eres un experto en Python que sugiere mejoras y corrige errores en bots de trading. Responde con el nuevo código en bloque de código y con comentarios explicativos de lo que has mejorado."},
        {"role": "user", "content": f"Este es el código actual del bot de trading:
{code_to_analyze}

Sugiere una mejora o corrección. Responde solo con código dentro de bloque ```python y con comentarios dentro del código explicando los cambios."}
    ]
)

# Limpiar el resultado del bloque ```python
sugg = response.choices[0].message.content.strip()
sugg_clean = "
".join([line for line in sugg.splitlines() if not line.strip().startswith("```")])

# Guardar la sugerencia
with open("suggestion.txt", "w", encoding="utf-8") as f:
    f.write(sugg_clean)

print("✅ Sugerencia generada y guardada.")
