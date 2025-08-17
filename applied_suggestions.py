# Archivo de pruebas para sugerencias automáticas de GPT
\n# === INICIO GPT SUGERENCIA ===
import os

# Asegúrate de que la variable de entorno TRADIER_API_KEY está configurada
try:
    TRADIER_API_KEY = os.environ['TRADIER_API_KEY']
except KeyError:
    raise KeyError("La variable de entorno TRADIER_API_KEY no está configurada. Asegúrate de definirla antes de ejecutar el script.")

# Resto del código que utiliza TRADIER_API_KEY...

Para el entorno:
env:
  TRADIER_API_KEY: ${{ secrets.TRADIER_API_KEY }}\n# === FIN GPT SUGERENCIA ===
\n# === INICIO GPT SUGERENCIA ===
import os

# Asegúrate de que la variable de entorno 'TRADIER_API_KEY' está definida
tradier_api_key = os.environ.get("TRADIER_API_KEY")
if tradier_api_key is None:
    raise ValueError("La variable de entorno 'TRADIER_API_KEY' no está definida.")

# Resto del script
\n# === FIN GPT SUGERENCIA ===
