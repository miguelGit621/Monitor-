from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração do fuso horário de Brasília
fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora_br = datetime.now(fuso_br)

hoje = agora_br.strftime("%Y-%m-%d")
amanha = (agora_br + timedelta(days=1)).strftime("%Y-%m-%d")

# 2. Configuração do ntfy (substitua pelo nome do seu tópico se for diferente)
NTFY_TOPIC = "notificacoes_b3_carteira_completa" 

def enviar_ntfy(mensagem):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(url, data=mensagem.encode('utf-8'))
    except Exception as e:
        print(f"Erro ao enviar ntfy: {e}")

# 3. Lista de ações para monitorar (adicione ou remova seus tickers aqui)
CARTEIRA = ["VALE3", "PETR4", "BBAS3", "ITSA4", "TAEE11"]

print(f"--- Iniciando monitoramento em {hoje} ---")

# 4. Varredura dos ativos na API da BRAPI
for ticker in CARTEIRA:
    url = f"https://brapi.dev/api/quote/{ticker}?dividends=true"
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            continue
            
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            continue
            
        proventos = results[0].get("dividendsData", {}).get("cashDividends", [])
        
        for provento in proventos:
            # Pega a data da API
            data_raw = provento.get("dateCom") or provento.get("approvedOn") or ""
            
            # LIMPEZA CRUCIAL: Pega apenas os 10 primeiros caracteres (YYYY-MM-DD)
            data_com_limpa = data_raw[:10]
            
            tipo = provento.get("assetIssued", "Provento")
            valor = provento.get("rate", 0)

            # Comparação
            if data_com_limpa == hoje:
                msg = f"🚨 DATA COM HOJE ({hoje}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor:.2f}"
                print(msg)
                enviar_ntfy(msg)
                
            elif data_com_limpa == amanha:
                msg = f"⚠️ DATA COM AMANHÃ ({amanha}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor:.2f}"
                print(msg)
                enviar_ntfy(msg)

    except Exception as e:
        print(f"Erro ao processar {ticker}: {e}")

print("--- Varredura finalizada ---")
