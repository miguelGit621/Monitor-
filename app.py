from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração de Fuso Horário do Brasil
fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora_br = datetime.now(fuso_br)

hoje = agora_br.strftime("%Y-%m-%d")
amanha = (agora_br + timedelta(days=1)).strftime("%Y-%m-%d")

# 2. Configuração do ntfy (confirme o nome do seu tópico)
NTFY_TOPIC = "notificacoes_b3_carteira_completa" 

def enviar_ntfy(mensagem):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        requests.post(url, data=mensagem.encode('utf-8'))
    except Exception as e:
        print(f"Erro ao enviar ntfy: {e}")

# 3. Sua Lista de Ações
CARTEIRA = ["VALE3", "PETR4", "BBAS3", "ITSA4", "TAEE11"]

# Cabeçalho para simular um navegador real (evita bloqueio 403 do Status Invest)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"--- Iniciando monitoramento em {hoje} ---")

for ticker in CARTEIRA:
    # Endpoint de proventos do Status Invest
    url = f"https://statusinvest.com.br/acao/companydividendreceiptlist?ticker={ticker}&type=1"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code != 200:
            print(f"Aviso: Não foi possível acessar dados de {ticker} (Status: {response.status_code})")
            continue
            
        data = response.json()
        
        # O Status Invest retorna a lista de proventos na chave 'result'
        proventos = data.get("result", {}).get("earnings", [])
        
        for provento in proventos:
            # Pega a Data COM (formato que vem da API: DD/MM/YYYY)
            data_com_br = provento.get("dateCom", "")
            
            if not data_com_br:
                continue
                
            # Converte DD/MM/YYYY para YYYY-MM-DD para comparar com 'hoje'
            try:
                data_com_dt = datetime.strptime(data_com_br, "%d/%m/%Y")
                data_com_iso = data_com_dt.strftime("%Y-%m-%d")
            except ValueError:
                continue

            tipo = provento.get("earningType", "Provento")
            valor = provento.get("resultAbsoluteValue", 0)

            # Comparação com Hoje e Amanhã
            if data_com_iso == hoje:
                msg = f"🚨 DATA COM HOJE ({hoje}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor:.2f}"
                print(msg)
                enviar_ntfy(msg)
                
            elif data_com_iso == amanha:
                msg = f"⚠️ DATA COM AMANHÃ ({amanha}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor:.2f}"
                print(msg)
                enviar_ntfy(msg)

    except Exception as e:
        print(f"Erro ao processar {ticker}: {e}")

print("--- Varredura finalizada ---")
