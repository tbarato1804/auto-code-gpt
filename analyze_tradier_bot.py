import os
import openai

# Inicializa el cliente con tu API Key
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Recolectar todos los .py del repo de trading ---
code_to_analyze = ""
for root, _, files in os.walk("tradier"):
    for file in files:
        if file.endswith(".py") and not file.startswith("test_"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                contenido = f.read()
                code_to_analyze += f"\n\n# === Archivo: {path} ===\n{contenido}"

# --- Prompt para obtener mejora y comentarios ---
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": (
                "Eres un experto en Python y trading algorítmico. Vas a sugerir una mejora clara para este código.\n"
                "- La sugerencia debe estar en un bloque de código completo.\n"
                "- Usa comentarios explicativos sobre los cambios que haces.\n"
                "- No repitas todo el código del bot, solo la función o sección modificada.\n"
                "- Si encuentras errores, corrígelos también."
            )
        },
        {
            "role": "user",
            "content": f"Este es el código actual del bot de trading:\n{code_to_analyze}\n\nSugiéreme una mejora o corrección útil, con comentarios."
        }
    ]
)

# --- Limpiar y guardar la sugerencia como .py ---
sugg = response.choices[0].message.content.strip()
sugg_clean = "\n".join([line for line in sugg.splitlines() if not line.strip().startswith("```")])

with open("suggestion.txt", "w", encoding="utf-8") as f:
    f.write(sugg_clean)

print("✅ Sugerencia generada y guardada.")
