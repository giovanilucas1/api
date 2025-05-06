from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# CONFIGURAÇÕES PARANÁ BANCO
client_id = 'alcif-s-bellato'
client_secret = '64y8cX5dmxYovd4tXTmed38Lbh5FMqJB'
username = 'alcif-mbr2'
password = '^L7i_O5c#A2y'

# URLS
url_auth = "https://api-marketplace.paranabanco.com.br/v1/auth/token"
url_saldo = "https://api-marketplace.paranabanco.com.br/v1/fgts/saque-aniversario/saldo-disponivel"
url_digisac = "https://belmocredito.digisac.biz/api/v1/messages"

# TOKEN FIXO OU DEIXE VAZIO SE FOR USAR AUTENTICAÇÃO POR HEADER
token_digisac = "7380291ffe0914b17d7b6ddde0a09db251903b12"

# TAXAS
taxa_mensal = 0.0179
taxa_anual = ((1 + taxa_mensal) ** 12 - 1) * 100

def gerar_token():
    payload = {
        'grant_type': 'password',
        'scope': 'openid',
        'client_id': client_id,
        'client_secret': client_secret,
        'username': username,
        'password': password
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Client-Id': client_id
    }
    response = requests.post(url_auth, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

def consultar_saldo(token, cpf, quantidade_periodos):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'X-Client-Id': client_id
    }
    payload = {
        "cpf": cpf,
        "quantidadeDePeriodos": quantidade_periodos
    }
    response = requests.post(url_saldo, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def enviar_mensagem_para_digisac(contato_id, texto):
    headers = {
        "Authorization": f"Bearer {token_digisac}",
        "Content-Type": "application/json"
    }
    payload = {
        "contactId": contato_id,
        "type": "text",
        "content": texto
    }
    response = requests.post(url_digisac, json=payload, headers=headers)
    print("📤 Enviado para Digisac:", response.status_code, response.text)

@app.route("/", methods=["POST"])
def receber_webhook():
    try:
        data = request.get_json()
        cpf = data["data"]["message"]["text"]
        contato_id = data["data"]["contactId"]

        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            enviar_mensagem_para_digisac(contato_id, "❌ CPF inválido. Envie um CPF com 11 dígitos.")
            return jsonify({"status": "erro", "mensagem": "CPF inválido"}), 400

        try:
            token = gerar_token()
            consultar_saldo(token, cpf, 6)
            enviar_mensagem_para_digisac(contato_id, "✅ CPF válido. Simulação em andamento.")
            return jsonify({"status": "ok", "mensagem": "CPF válido"}), 200
        except:
            enviar_mensagem_para_digisac(contato_id, "❌ CPF não encontrado ou sem saldo disponível.")
            return jsonify({"status": "erro", "mensagem": "CPF inválido no banco"}), 404

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

@app.route("/", methods=["GET"])
def status():
    return "✅ API ativa para receber webhook do Digisac"
