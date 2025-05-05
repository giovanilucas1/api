from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["POST"])
def validar_cpf():
    try:
        data = request.get_json()
        print("📩 JSON recebido:", data)

        # Tenta capturar CPF de vários pontos do corpo
        cpf = None
        if data.get("command") == "simular_fgts":
            cpf = data.get("message", {}).get("text")
        if not cpf:
            cpf = data.get("contact", {}).get("document") or data.get("cpf")

        print("🧠 CPF detectado:", cpf)

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
        print("❌ ERRO AO PROCESSAR:", e)
        return jsonify({
            "command": "erro",
            "message": f"❌ Erro ao processar CPF: {str(e)}"
        })

@app.route("/", methods=["GET"])
def status():
    return "✅ API ativa e validando CPFs para o Webhook da Digisac."
