from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/validar-cpf', methods=['POST'])
def validar_cpf():
    data = request.get_json()
    cpf = data.get('cpf')

    if cpf:
        print(f"CPF recebido: {cpf}")

        # Aqui você pode validar ou salvar o CPF se quiser

        # Resposta com uma flag e uma mensagem para o bot enviar
        return jsonify({
            "flag": "cpf_ok",  # Essa flag pode ser usada no bot como gatilho
            "mensagem": f"✅ CPF {cpf} enviado com sucesso!"
        })
    else:
        return jsonify({
            "flag": "cpf_invalido",
            "mensagem": "❌ CPF inválido. Tente novamente."
        }), 400

if __name__ == '__main__':
    app.run(port=5000)
