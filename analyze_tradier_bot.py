import os
import openai
import re
import py_compile

# Configuración
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
REPO_DIR = "tradier"
PATCH_FILE = "gpt_patch.py"
ERROR_FILE = "syntax_error.txt"

# Palabras clave para ignorar sugerencias inútiles
IGNORE_KEYWORDS = [
    "os.getenv(\"TRADIER_API_KEY\")",
    "La variable de entorno 'TRADIER_API_KEY' no está establecida",
    "asegúrate de que la variable de entorno",
    "comprobar si TRADIER_API_KEY está definida",
]

def should_ignore_suggestion(suggestion: str) -> bool:
    return any(keyword in suggestion for keyword in IGNORE_KEYWORDS)

# Cambiar al directorio del repo clonado
os.chdir(REPO_DIR)

# Leer todos los .py del repo
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

# Validar contenido
if not code_to_analyze.strip():
    print("⚠️ No se encontró código para analizar.")
    exit(0)

# Solicitar sugerencia a OpenAI
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

# Extraer solo el bloque de código Python
match = re.search(r"```python(.*?)```", sugg, re.DOTALL)
clean_code = match.group(1).strip() if match else ""

# Volver a raíz y guardar sugerencia
os.chdir("..")

if clean_code and not should_ignore_suggestion(clean_code):
    with open(PATCH_FILE, "w", encoding="utf-8") as f:
        f.write(clean_code)
    print("✅ Sugerencia generada y guardada.")

    # Verificar sintaxis del parche
    try:
        py_compile.compile(PATCH_FILE, doraise=True)
        print("✅ Sintaxis del parche verificada correctamente.")
    except py_compile.PyCompileError as e:
        with open(ERROR_FILE, "w", encoding="utf-8") as f:
            f.write("❌ Error de sintaxis en la sugerencia generada. El parche no será aplicado automáticamente.\n\n")
            f.write(str(e))
        print("❌ Error de sintaxis detectado. Se ha generado syntax_error.txt.")
        exit(1)
else:
    with open(ERROR_FILE, "w", encoding="utf-8") as f:
        f.write("⚠️ La sugerencia fue ignorada por ser irrelevante o vacía.\n\n")
        f.write(sugg)
    print("⚠️ Sugerencia ignorada o inválida. Se ha generado syntax_error.txt.")
    exit(1)
