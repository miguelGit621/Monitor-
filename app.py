from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração de Fuso Horário do Brasil
fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora_br = datetime.now(fuso_br)

dt_hoje = agora_br.date()
dt_fim = dt_hoje + timedelta(days=7)

NTFY_TOPIC = "notificacoes_b3_carteira_completa" 

def enviar_ntfy(mensagem):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        res = requests.post(url, data=mensagem.encode('utf-8'))
        print(f"Status NTFY enviado: {res.status_code}")
    except Exception as e:
        print(f"Erro ao enviar ntfy: {e}")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*'
}

def converter_para_data(data_str):
    if not data_str or data_str == "-":
        return None
    data_clean = str(data_str).split("T")[0].split(" ")[0].strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(data_clean, fmt).date()
        except ValueError:
            pass
    return None

def identificar_tipo_provento(raw_tipo):
    if not raw_tipo:
        return "Provento", "💰"
    tipo_upper = str(raw_tipo).upper()
    if "JCP" in tipo_upper or "JUROS" in tipo_upper:
        return "JCP (Juros s/ Capital Próprio)", "🏛️"
    elif "DIVIDENDO" in tipo_upper:
        return "Dividendo", "💵"
    elif "AMORTI" in tipo_upper:
        return "Amortização", "🔄"
    else:
        return str(raw_tipo).title(), "💰"

def buscar_proventos_investnews():
    print(f"=== Varredura B3 via InvestNews ({dt_hoje.strftime('%d/%m/%Y')} a {dt_fim.strftime('%d/%m/%Y')}) ===")
    
    # Endpoint público do InvestNews (Dados B3 sem bloqueio Cloudflare)
    url = "https://api.investnews.com.br/wp-json/investnews/v1/proventos"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        print(f"Status da resposta: {response.status_code}")

        if response.status_code == 200:
            dados = response.json()
            eventos = dados.get("data", []) if isinstance(dados, dict) else dados
            print(f"Total de proventos retornados na API: {len(eventos)}")
            
            notificados = 0
            for ev in eventos:
                ticker = str(ev.get("ticker") or ev.get("code") or ev.get("symbol") or "").upper().strip()
                data_com = converter_para_data(ev.get("data_com") or ev.get("dateCom"))
                data_pag = converter_para_data(ev.get("data_pagamento") or ev.get("paymentDate"))
                tipo_nome, icone = identificar_tipo_provento(ev.get("tipo") or ev.get("earningType"))
                valor = ev.get("valor") or ev.get("value") or 0

                # 1. Alerta de Data COM
                if data_com and dt_hoje <= data_com <= dt_fim:
                    dias = (data_com - dt_hoje).days
                    prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                    msg = f"{prefixo} ({data_com.strftime('%d/%m/%Y')}) - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}"
                    print(f"-> Disparando Data COM: {ticker}")
                    enviar_ntfy(msg)
                    notificados += 1

                # 2. Alerta de Pagamento
                if data_pag and dt_hoje <= data_pag <= dt_fim:
                    dias = (data_pag - dt_hoje).days
                    prefixo = "✅ PAGAMENTO HOJE" if dias == 0 else ("🗓️ PAGAMENTO AMANHÃ" if dias == 1 else f"💰 PAGAMENTO EM {dias} DIAS")
                    msg = f"{prefixo} ({data_pag.strftime('%d/%m/%Y')}) - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}"
                    print(f"-> Disparando Pagamento: {ticker}")
                    enviar_ntfy(msg)
                    notificados += 1

            print(f"=== Varredura concluída. Total de notificações enviadas: {notificados} ===")
            return True
        else:
            print(f"Erro na API InvestNews: {response.status_code}")
            return False

    except Exception as e:
        print(f"Erro na requisição: {e}")
        return False

if __name__ == "__main__":
    buscar_proventos_investnews()
