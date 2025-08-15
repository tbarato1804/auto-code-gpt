
# test_bot.py
import json

def run_test():
    result = {
        "status": "fail",
        "error": "KeyError: TRADIER_API_KEY",
        "description": "El script no encontró la variable de entorno necesaria para autenticarse con la API de Tradier."
    }
    with open("example_result.json", "w") as f:
        json.dump(result, f, indent=2)
    print("✅ Simulación de prueba completada.")

if __name__ == "__main__":
    run_test()
