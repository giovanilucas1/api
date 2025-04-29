from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def root():
    return "✅ API FGTS online!"

@app.route("/fgts", methods=["POST"])
def simular_fgts():
    try:
        data = request.json
        cpf = data.get("cpf")
        if not cpf or len(cpf) != 11:
            return jsonify({"erro": True, "mensagem": "CPF inválido."}), 400

        # Aqui você chama suas funções internas:
        # token = gerar_token()
        # resultado = consultar_saldo(token, cpf, ...)

        return jsonify({
            "mensagem": f"Simulação recebida para CPF {cpf}.",
            "teste": True
        })

    except Exception as e:
        return jsonify({"erro": True, "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run()
