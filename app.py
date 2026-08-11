from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração de Fuso Horário do Brasil
fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora_br = datetime.now(fuso_br)

dt_hoje = agora_br.date()
dt_amanha = dt_hoje + timedelta(days=1)

# Janela ampla de busca (3 dias atrás até 7 dias à frente)
dt_inicio = dt_hoje - timedelta(days=3)
dt_fim = dt_hoje + timedelta(days=7)

# Formato exigido na URL pelo Status Invest: DD/MM/YYYY
inicio_url = dt_inicio.strftime("%d/%m/%Y")
fim_url = dt_fim.strftime("%d/%m/%Y")

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

def converter_para_data(data_str):
    """Converte strings de data (DD/MM/YYYY ou YYYY-MM-DD) em objeto date do Python"""
    if not data_str:
        return None
    data_str = data_str.split("T")[0].strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(data_str, fmt).date()
        except ValueError:
            pass
    return None

def obter_dy_str(evento):
    """Extrai e formata o Dividend Yield (%) do evento se disponível na API"""
    dy = evento.get("dy") or evento.get("dividendYield") or evento.get("yield")
    if dy is not None:
        try:
            dy_float = float(dy)
            return f"{dy_float:.2f}%"
        except (ValueError, TypeError):
            pass
    return "N/D"

print(f"--- Varredura Geral B3 em {dt_hoje.strftime('%d/%m/%Y')} ---")

# ==========================================
# 1. BUSCA DE DATAS COM
# ==========================================
url_com = f"https://statusinvest.com.br/acao/getevents?dateCom.start={inicio_url}&dateCom.end={fim_url}&byDateCom=true"

try:
    res_com = requests.get(url_com, headers=HEADERS, timeout=15)
    if res_com.status_code == 200:
        eventos_com = res_com.json()
        print(f"Eventos de Data COM encontrados no período ({inicio_url} a {fim_url}): {len(eventos_com)}")
        
        for evento in eventos_com:
            ticker = evento.get("code", "N/A")
            raw_date = evento.get("dateCom", "")
            data_evento = converter_para_data(raw_date)
            
            tipo = evento.get("earningType", "Provento")
            valor = evento.get("resultAbsoluteValue", 0)
            dy_str = obter_dy_str(evento)

            if data_evento == dt_hoje:
                msg = f"🚨 DATA COM HOJE ({dt_hoje.strftime('%d/%m/%Y')}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}\nDY: {dy_str}"
                print(f"-> ENCONTRADO: {msg}")
                enviar_ntfy(msg)
            elif data_evento == dt_amanha:
                msg = f"⚠️ DATA COM AMANHÃ ({dt_amanha.strftime('%d/%m/%Y')}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}\nDY: {dy_str}"
                print(f"-> ENCONTRADO: {msg}")
                enviar_ntfy(msg)
            else:
                print(f" - {ticker}: Data COM em {raw_date} (fora de hoje/amanhã)")
except Exception as e:
    print(f"Erro na busca de Data COM: {e}")

# ==========================================
# 2. BUSCA DE DATAS DE PAGAMENTO
# ==========================================
url_pagamento = f"https://statusinvest.com.br/acao/getevents?paymentDate.start={inicio_url}&paymentDate.end={fim_url}&byPaymentDate=true"

try:
    res_pag = requests.get(url_pagamento, headers=HEADERS, timeout=15)
    if res_pag.status_code == 200:
        eventos_pag = res_pag.json()
        print(f"Eventos de Pagamento encontrados no período ({inicio_url} a {fim_url}): {len(eventos_pag)}")
        
        for evento in eventos_pag:
            ticker = evento.get("code", "N/A")
            raw_date = evento.get("paymentDate", "")
            data_evento = converter_para_data(raw_date)
            
            tipo = evento.get("earningType", "Provento")
            valor = evento.get("resultAbsoluteValue", 0)
            dy_str = obter_dy_str(evento)

            if data_evento == dt_hoje:
                msg = f"💰 PAGAMENTO HOJE ({dt_hoje.strftime('%d/%m/%Y')}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}\nDY: {dy_str}"
                print(f"-> ENCONTRADO: {msg}")
                enviar_ntfy(msg)
            elif data_evento == dt_amanha:
                msg = f"💵 PAGAMENTO AMANHÃ ({dt_amanha.strftime('%d/%m/%Y')}) - {ticker}\nTipo: {tipo}\nValor: R$ {valor}\nDY: {dy_str}"
                print(f"-> ENCONTRADO: {msg}")
                enviar_ntfy(msg)
except Exception as e:
    print(f"Erro na busca de Data de Pagamento: {e}")

print("--- Varredura finalizada ---")
