from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receber_webhook():
    try:
        # Exibe o corpo bruto recebido
        raw_data = request.get_data(as_text=True)
        print("📦 RAW BODY RECEBIDO:", raw_data)

        # Tenta converter o corpo em JSON
        data = request.get_json(force=True, silent=True)
        if not data:
            return jsonify({
                "command": "erro",
                "message": "❌ JSON malformado ou vazio."
            })

        print("🧠 JSON PARSEADO:", data)

        command = data.get("command")
        print("📌 Comando recebido:", command)

        cpf = None

        # Verifica se o comando é o esperado e tenta extrair o CPF
        if command == "simular_fgts":
            cpf = (
                data.get("message", {}).get("text") or
                data.get("contact", {}).get("document") or
                data.get("cpf")
            )

        print("🧾 CPF detectado:", cpf)

        # Validação básica do CPF
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return jsonify({
                "command": "cpf_invalido",
                "message": "❌ CPF inválido. Envie um CPF com 11 dígitos numéricos."
            })

        # CPF válido
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
