from flask import Flask, request, jsonify
import requests
import datetime

app = Flask(__name__)

# CONFIGURAÇÕES
client_id = 'alcif-s-bellato'
client_secret = '64y8cX5dmxYovd4tXTmed38Lbh5FMqJB'
username = 'alcif-mbr2'
password = '^L7i_O5c#A2y'

url_auth = "https://api-marketplace.paranabanco.com.br/v1/auth/token"
url_saldo = "https://api-marketplace.paranabanco.com.br/v1/fgts/saque-aniversario/saldo-disponivel"

# Taxas
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

def consultar_saldo(token, cpf, quantidade_periodos=10):
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

@app.route("/", methods=["POST"])
def validar_cpf():
    try:
        data = request.get_json()
        print("📩 JSON recebido:", data)

        # Tenta pegar o CPF de várias formas
        cpf = None
        if data.get("command") == "simular_fgts":
            cpf = data.get("message", {}).get("text")
        if not cpf:
            cpf = data.get("contact", {}).get("document") or data.get("cpf")

        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return jsonify({
                "command": "cpf_invalido",
                "message": "❌ CPF inválido. Envie um CPF com 11 dígitos numéricos."
            })

        token = gerar_token()
        saldo = consultar_saldo(token, cpf)

        if saldo.get("saldoTotal", 0) <= 0:
            return jsonify({
                "command": "cpf_invalido",
                "message": "❌ CPF sem saldo disponível para empréstimo."
            })

        return jsonify({
            "command": "cpf_valido",
            "message": f"✅ CPF {cpf} validado com sucesso! Saldo: R$ {round(saldo['saldoTotal'], 2)}"
        })

    except Exception as e:
        print("❌ ERRO AO PROCESSAR:", e)
        return jsonify({
            "command": "erro",
            "message": f"❌ Erro ao processar CPF: {str(e)}"
        })

@app.route("/", methods=["GET"])
def status():
    return "✅ API ativa e esperando Webhook da Digisac."
