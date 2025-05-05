@app.route("/webhook", methods=["POST"])
def receber_digisac():
    try:
        data = request.get_json()

        # Ajuste aqui de acordo com o JSON real da Digisac
        cpf = data.get("contact", {}).get("document")
        if not cpf or len(cpf) != 11 or not cpf.isdigit():
            return jsonify({"message": "❌ CPF inválido. Envie um CPF válido com 11 dígitos."})

        quantidade = 10  # fixo ou você pode mudar conforme o texto da mensagem

        token = gerar_token()
        saldo_data = consultar_saldo(token, cpf, quantidade)
        resposta = montar_resposta(saldo_data, quantidade)

        # Retorno em forma de texto para o cliente
        if resposta["erro"]:
            return jsonify({"message": resposta["mensagem"]})

        resumo = resposta["resumo"]
        parcelas_txt = "\n".join(
            [f"📅 {p['vencimento']}: R$ {p['valor_parcela']}" for p in resposta["parcelas_detalhadas"]]
        )

        mensagem = (
            f"{resposta['mensagem']}\n"
            f"💰 Valor do Empréstimo: R$ {resumo['valor_emprestimo']}\n"
            f"📊 Total a Pagar: R$ {resumo['valor_total_pago']}\n"
            f"🧾 Parcelas: {resumo['parcelas']}\n"
            f"{parcelas_txt}"
        )

        return jsonify({"message": mensagem})

    except Exception as e:
        return jsonify({"message": f"❌ Erro interno: {str(e)}"}), 500
