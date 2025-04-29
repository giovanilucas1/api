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

# Taxas fixas
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

def montar_resposta(saldo_data, quantidade_periodos):
    saldo_total = saldo_data.get("saldoTotal", 0)
    saldos_por_periodo = saldo_data.get("saldosPorPeriodo", [])

    if saldo_total <= 0:
        return {"erro": True, "mensagem": "❌ Cliente sem saldo disponível para simulação."}

    parcelas = []
    for idx, periodo in enumerate(saldos_por_periodo, 1):
        data_repasse = periodo.get('dataPrevistaParaORepasse', 'N/A')
        saldo_disponivel = periodo.get('saldoDisponivelParaReserva', 0)

        vencimento = 'N/A'
        if data_repasse != 'N/A':
            vencimento = datetime.datetime.strptime(data_repasse, "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%m/%Y")

        valor_parcela = (saldo_disponivel * taxa_mensal) / (1 - (1 + taxa_mensal) ** (-quantidade_periodos))
        parcelas.append({
            "parcela": idx,
            "vencimento": vencimento,
            "valor_parcela": round(valor_parcela, 2),
            "valor_reservado": round(saldo_disponivel, 2)
        })

    valor_iof = 2.87  # Exemplo fixo
    valor_emprestimo = saldo_total * 0.6313
    valor_parcela_geral = (valor_emprestimo * taxa_mensal) / (1 - (1 + taxa_mensal) ** (-quantidade_periodos))
    valor_total_pago = valor_parcela_geral * quantidade_periodos
    juros_total = valor_total_pago - valor_emprestimo

    return {
        "erro": False,
        "mensagem": "✅ Simulação realizada com sucesso.",
        "resumo": {
            "valor_emprestimo": round(valor_emprestimo, 2),
            "saldo_reservado": round(saldo_total, 2),
            "taxa_anual": round(taxa_anual, 2),
            "taxa_mensal": round(taxa_mensal * 100, 2),
            "valor_iof": round(valor_iof, 2),
            "parcelas": quantidade_periodos,
            "valor_total_pago": round(valor_total_pago, 2),
            "juros_total": round(juros_total, 2)
        },
        "parcelas_detalhadas": parcelas
    }

@app.route("/", methods=["GET"])
def home():
    return "✅ API FGTS - ParanáBanco online!"

@app.route("/fgts", methods=["POST"])
def simular_fgts():
    try:
        data = request.get_json()
        cpf = data.get("cpf")
        quantidade = int(data.get("periodos", 10))

        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return jsonify({"erro": True, "mensagem": "CPF inválido. Envie 11 dígitos numéricos."}), 400

        token = gerar_token()
        saldo_data = consultar_saldo(token, cpf, quantidade)
        resposta = montar_resposta(saldo_data, quantidade)
        return jsonify(resposta)

    except Exception as e:
        return jsonify({"erro": True, "mensagem": str(e)}), 500

if __name__ == "__main__":
    app.run()
