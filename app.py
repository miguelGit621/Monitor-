from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração de Fuso Horário do Brasil
fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora_br = datetime.now(fuso_br)

hoje = agora_br.strftime("%Y-%m-%d")
amanha = (agora_br + timedelta(days=1)).strftime("%Y-%m-%d")

# Formato brasileiro (DD/MM/YYYY) para comparar com o retorno da API
hoje_br_fmt = agora_br.strftime("%d/%m/%Y")
amanha_br_fmt = (agora_br + timedelta(days=1)).strftime("%d/%m/%Y")

# 2. Configuração do ntfy
NTFY_TOPIC = "notificacoes_b3_carteira_completa" 

def enviar_ntfy(mensagem):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(url, data=mensagem.encode('utf-8'))
    except Exception as e:
        print(f"Erro ao enviar ntfy: {e}")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

print(f"--- Varredura Geral B3 em {hoje_br_fmt} ---")

# ==========================================
# 1. BUSCA DE DATAS COM (HOJE E AMANHÃ)
# ==========================================
url_com = f"https://statusinvest.com.br/acao/getevents?dateCom.start={hoje}&dateCom.end={amanha}&byDateCom=true"

try:
    res_com = requests.get(url_com, headers=HEADERS, timeout=15)
    if res_com.status_code == 200:
        eventos_com = res_com.json()
        for evento in eventos_com:
            ticker = evento.get("code", "N/A")
            data_com = evento.get("dateCom", "")
            tipo = evento.get("earningType", "Provento")
            valor = evento.get("resultAbsoluteValue", 0)

            if data_com == hoje_br_fmt:
                msg = f"🚨 DATA COM HOJE ({hoje_br_fmt}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}"
                print(msg)
                enviar_ntfy(msg)
            elif data_com == amanha_br_fmt:
                msg = f"⚠️ DATA COM AMANHÃ ({amanha_br_fmt}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}"
                print(msg)
                enviar_ntfy(msg)
except Exception as e:
    print(f"Erro na busca de Data COM: {e}")

# ==========================================
# 2. BUSCA DE DATAS DE PAGAMENTO (HOJE E AMANHÃ)
# ==========================================
url_pagamento = f"https://statusinvest.com.br/acao/getevents?paymentDate.start={hoje}&paymentDate.end={amanha}&byPaymentDate=true"

try:
    res_pag = requests.get(url_pagamento, headers=HEADERS, timeout=15)
    if res_pag.status_code == 200:
        eventos_pag = res_pag.json()
        for evento in eventos_pag:
            ticker = evento.get("code", "N/A")
            data_pag = evento.get("paymentDate", "")
            tipo = evento.get("earningType", "Provento")
            valor = evento.get("resultAbsoluteValue", 0)

            if data_pag == hoje_br_fmt:
                msg = f"💰 PAGAMENTO HOJE ({hoje_br_fmt}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}"
                print(msg)
                enviar_ntfy(msg)
            elif data_pag == amanha_br_fmt:
                msg = f"💵 PAGAMENTO AMANHÃ ({amanha_br_fmt}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}"
                print(msg)
                enviar_ntfy(msg)
except Exception as e:
    print(f"Erro na busca de Data de Pagamento: {e}")

print("--- Varredura finalizada ---")
