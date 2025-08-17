# Auto-Code GPT con Historial

Este flujo automatiza:

1. Ejecutar prueba simulada (`test_bot.py`)
2. Obtener sugerencia desde OpenAI (`send_to_openai.py`)
3. Guardar:
   - `suggestion.txt` (última sugerencia)
   - `history/suggestion-YYYYMMDD-HHMMSS.txt` (todas las sugerencias)
4. Formatear, aplicar e insertar sugerencia al final de `applied_suggestions.py`
5. Commit y push automático
