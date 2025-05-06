from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    try:
        # 🔍 Mostra o corpo cru da requisição
        raw = request.data.decode("utf-8", errors="replace")
        print("🔍 RAW BODY RECEBIDO:\n", raw)

        # 📦 Tenta converter para JSON, mesmo que incompleto
        data = request.get_json(force=True, silent=True) or {}
        print("📦 JSON PARSEADO:", data)

        # 📌 Detecta comando (se for necessário)
        comando = data.get("command", "")
        print("📌 Comando recebido:", comando)

        # 🧠 Tenta detectar CPF de várias formas
        cpf = data.get("cpf") or \
              data.get("message", {}).get("text") or \
              data.get("contact", {}).get("document")

        print("🧠 CPF detectado:", cpf)

        # Só para teste: responde que chegou
        return jsonify({
            "status": "ok",
            "mensagem": "📬 Webhook recebido com sucesso!",
            "comando": comando,
            "cpf": cpf
        })

    except Exception as e:
        print("❌ ERRO AO PROCESSAR:", str(e))
        return jsonify({
            "status": "erro",
            "mensagem": f"❌ Erro ao processar webhook: {str(e)}"
        }), 500

@app.route("/", methods=["GET"])
def status():
    return "✅ API de teste - aguardando Webhook da Digisac."
