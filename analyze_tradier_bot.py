import os
import openai

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cambiar al directorio del repo clonado
os.chdir("tradier")

code_to_analyze = ""
for root, _, files in os.walk("."):
    for file in files:
        if file.endswith(".py") and not file.startswith("test_"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if content.strip():
                        code_to_analyze += f"\n\n# === Archivo: {path} ===\n{content}"
            except Exception as e:
                print(f"❌ Error al leer {path}: {e}")

if not code_to_analyze.strip():
    print("⚠️ No se encontró código para analizar.")
    exit(0)

# Llamada a OpenAI
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "Eres un experto en Python. Vas a analizar el siguiente bot de trading y sugerir mejoras claras, explicadas en los comentarios del código.",
        },
        {
            "role": "user",
            "content": f"Aquí está el código actual:\n{code_to_analyze}\n\nSugiéreme una mejora o corrección como código funcional dentro de un bloque ```python y con comentarios explicativos.",
        },
    ],
)

sugg = response.choices[0].message.content.strip()
sugg_clean = "\n".join([line for line in sugg.splitlines() if not line.strip().startswith("```")])

# Volver a la raíz del flujo y guardar
os.chdir("..")
with open("suggestion.txt", "w", encoding="utf-8") as f:
    f.write(sugg_clean)

print("✅ Sugerencia generada y guardada.")
