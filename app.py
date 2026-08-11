from datetime import datetime
import time
import requests

# ==========================================
# CONFIGURAÇÕES
# ==========================================
# Insira seu token gratuito do brapi.dev (obtenha em https://brapi.dev)
BRAPI_TOKEN = "SEU_TOKEN_AQUI"

# Tópico para notificações via ntfy.sh (pode ser qualquer nome único)
NTFY_TOPIC = "notificacoes_b3_carteira_completa"


def obter_todos_os_tickers():
    """Busca a lista completa de tickers ativos na B3 via API."""
    url = f"https://brapi.dev/api/quote/list?token={BRAPI_TOKEN}"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            dados = response.json()
            stocks = dados.get("stocks", [])
            # Filtra e extrai apenas os códigos dos tickers (Ações, FIIs, BDRs, ETFs)
            tickers = [
                s.get("stock")
                for s in stocks
                if s.get("stock") and not s.get("stock").endswith("F")
            ]
            print(f"Total de {len(tickers)} tickers obtidos da B3.")
            return list(set(tickers))
    except Exception as err:
        print(f"Erro ao buscar lista de tickers: {err}")

    # Fallback: Caso a busca falhe, usa uma lista padrão com os principais ativos
    return ["PETR4", "VALE3", "BBAS3", "ITSA4", "MXRF11", "WEGE3", "HGLG11"]


def consultar_proventos_em_lote(tickers_lote):
    """Consulta proventos de até 20 tickers em uma única requisição."""
    str_tickers = "%2C".join(tickers_lote)
    url = f"https://brapi.dev/api/quote/{str_tickers}?dividends=true&token={BRAPI_TOKEN}"

    try:
        response = requests.get(url, timeout=25)
        if response.status_code == 200:
            dados = response.json()
            return dados.get("results", [])
    except Exception as err:
        print(f"Erro no lote de tickers: {err}")

    return []


def enviar_notificacao_push(mensagem):
    """Envia notificação push gratuita para o celular via ntfy.sh."""
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(
            url,
            data=mensagem.encode("utf-8"),
            headers={
                "Title": "Alerta B3 - Datas COM e Pagamentos",
                "Priority": "high",
                "Tags": "moneybag,chart_with_upwards_trend",
            },
            timeout=10,
        )
    except Exception as err:
        print(f"Erro ao enviar notificacao ntfy: {err}")


def verificar_eventos_do_dia():
    hoje = datetime.now().strftime("%Y-%m-%d")
    alertas_data_com = []
    alertas_pagamento = []

    print(f"Iniciando varredura completa da B3 para a data: {hoje}...")

    # 1. Obter todos os tickers da B3
    todos_tickers = obter_todos_os_tickers()

    # 2. Dividir em lotes de 20 tickers por chamada API
    TAMANHO_LOTE = 20
    lotes = [
        todos_tickers[i : i + TAMANHO_LOTE]
        for i in range(0, len(todos_tickers), TAMANHO_LOTE)
    ]

    for index, lote in enumerate(lotes):
        results = consultar_proventos_em_lote(lote)

        for ativo in results:
            ticker = ativo.get("symbol", "")
            proventos = ativo.get("dividendsData", {}).get("cashDividends", [])

            for p in proventos:
                tipo = p.get("label", "Provento")  # Dividendo, JCP, Amortização
                valor = p.get("rate", 0)

                # Formatação de datas retornadas (YYYY-MM-DD)
                data_com = (
                    p.get("approvedDate", "")[:10]
                    if p.get("approvedDate")
                    else ""
                )
                data_pagamento = (
                    p.get("paymentDate", "")[:10]
                    if p.get("paymentDate")
                    else ""
                )

                # Alerta se hoje for Data COM
                if data_com == hoje:
                    alertas_data_com.append(
                        f"• {ticker} ({tipo}): R$ {valor:.2f} | DATA COM"
                    )

                # Alerta se hoje for Data de Pagamento
                if data_pagamento == hoje:
                    alertas_pagamento.append(
                        f"• {ticker} ({tipo}): R$ {valor:.2f} | PAGAMENTO"
                    )

        # Pequena pausa entre requisições para evitar bloqueio de IP
        time.sleep(0.3)

    # 3. Montar e disparar a notificação se houver eventos hoje
    mensagem_final = ""
    if alertas_data_com:
        mensagem_final += (
            "📌 DATAS COM HOJE:\n" + "\n".join(alertas_data_com) + "\n\n"
        )
    if alertas_pagamento:
        mensagem_final += "💰 PAGAMENTOS HOJE:\n" + "\n".join(alertas_pagamento)

    if mensagem_final:
        print("Notificação montada com sucesso:\n", mensagem_final)
        enviar_notificacao_push(mensagem_final)
    else:
        print(
            "Varredura concluída. Nenhum evento de Data COM ou Pagamento identificado para hoje."
        )


if __name__ == "__main__":
    verificar_eventos_do_dia()
