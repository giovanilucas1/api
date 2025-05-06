from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    try:
        # Pega o corpo bruto da requisição (independente de estar certo)
        raw_data = request.data.decode("utf-8", errors="replace")
        print("📥 Corpo bruto recebido:\n", raw_data)

        # Tenta converter pra JSON
        data = request.get_json(force=True, silent=True) or {}
        print("📦 JSON decodificado:", data)

        # Verifica o comando
        comando = data.get("command", "")
        print("📌 Comando recebido:", comando)

        if comando != "simular_fgts":
            return jsonify({
                "command": "ignorado",
                "message": "📭 Comando não é 'simular_fgts', ignorado."
            })

        # Captura o CPF de diferentes lugares possíveis
        cpf = data.get("cpf") or \
              data.get("message", {}).get("text") or \
              data.get("contact", {}).get("document")

        print("🧠 CPF detectado:", cpf)

        # Validação básica do CPF
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return jsonify({
                "command": "cpf_invalido",
                "message": "❌ CPF inválido. Envie um CPF com 11 dígitos numéricos."
            })

        return jsonify({
            "command": "cpf_valido",
            "message": f"✅ CPF {cpf} validado com sucesso!"
        })

    except Exception as e:
        print("❌ ERRO GERAL:", e)
        return jsonify({
            "command": "erro",
            "message": f"❌ Erro ao processar requisição: {str(e)}"
        })

@app.route("/", methods=["GET"])
def status():
    return "✅ API ativa, aguardando comando 'simular_fgts' do webhook."
