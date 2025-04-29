from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/validar-cpf', methods=['POST'])
def validar_cpf():
    data = request.get_json()
    cpf = data.get('cpf')

    if cpf:
        print(f"CPF recebido: {cpf}")
        return jsonify({"mensagem": "Enviado"})
    else:
        return jsonify({"erro": "CPF não encontrado no payload"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
