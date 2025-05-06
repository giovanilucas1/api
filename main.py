from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receber_webhook():
    try:
        # Mostra o corpo bruto recebido
        raw = request.get_data(as_text=True)
        print("📦 RAW RECEBIDO:", raw)

        # Tenta interpretar como JSON
        try:
            data = request.get_json(force=True)
            print("🧠 JSON INTERPRETADO:", data)
        except Exception as e:
            print("❌ Erro ao interpretar JSON:", e)
            data = None

        return jsonify({
            "status": "ok",
            "mensagem": "🧪 Webhook recebido com sucesso",
            "json_recebido": data,
            "raw_body": raw
        })

    except Exception as e:
        print("❌ ERRO GERAL:", str(e))
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao receber webhook: {str(e)}"
        })

@app.route("/", methods=["GET"])
def status():
    return "✅ API funcionando para testes de webhook Digisac"
