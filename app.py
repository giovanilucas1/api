from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Digisac Webhook Endpoint - substitua pela sua URL se for diferente
DIGISAC_WEBHOOK_URL = "https://hook.digisac.com.br/seu-webhook"

@app.route("/", methods=["POST"])
def receber_webhook():
    try:
        raw = request.get_data(as_text=True)
        print("📦 RAW RECEBIDO:", raw)

        data = request.get_json(force=True)
        print("🧠 JSON INTERPRETADO:", data)

        cpf = data.get("data", {}).get("message", {}).get("text")
        print("🧾 CPF recebido:", cpf)

        if cpf and cpf.isdigit() and len(cpf) == 11:
            status = "cpf_valido"
            msg = f"✅ CPF {cpf} validado com sucesso!"
        else:
            status = "cpf_invalido"
            msg = "❌ CPF inválido. Envie um com 11 dígitos numéricos."

        # Envia o webhook de volta para a Digisac
        webhook_payload = {
            "command": status,
            "message": msg
        }

        print("📡 Enviando de volta para Digisac:", webhook_payload)
        r = requests.post(DIGISAC_WEBHOOK_URL, json=webhook_payload)
        print("🔁 Status resposta:", r.status_code)

        return jsonify({
            "status": status,
            "mensagem": msg
        })

    except Exception as e:
        print("❌ ERRO GERAL:", str(e))
        return jsonify({
            "status": "erro",
            "mensagem": f"Erro ao processar: {str(e)}"
        })

@app.route("/", methods=["GET"])
def status():
    return "✅ API funcionando para testes de CPF Digisac"
