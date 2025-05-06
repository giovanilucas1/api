from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receber_webhook():
    try:
        raw_data = request.get_data(as_text=True)
        print("📦 RAW BODY RECEBIDO:", raw_data)

        data = request.get_json(force=True)
        print("🧠 JSON PARSEADO:", data)

        command = data.get("command")
        print("📌 Comando recebido:", command)

        # Tentativa de pegar o CPF
        cpf = None
        if command == "simular_fgts":
            cpf = data.get("message", {}).get("text") \
               or data.get("contact", {}).get("document") \
               or data.get("cpf")

        print("🧾 CPF detectado:", cpf)

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
        print("❌ ERRO AO PROCESSAR:", str(e))
        return jsonify({
            "command": "erro",
            "message": f"❌ Erro ao processar requisição: {str(e)}"
        })


@app.route("/", methods=["GET"])
def status():
    return "✅ API de teste ativa e aguardando chamadas da Digisac."
