# Archivo de pruebas para sugerencias automáticas de GPT
\n# 💡 Sugerencia automática generada por OpenAI
import os

# Asegúrate de que TRADIER_API_KEY esté en tus variables de entorno
tradier_api_key = os.getenv("TRADIER_API_KEY")
if not tradier_api_key:
    raise EnvironmentError(
        "La variable de entorno 'TRADIER_API_KEY' no está configurada"
    )

# Resto del script de trading que utiliza tradier_api_key
