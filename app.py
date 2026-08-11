from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração de Fuso Horário
fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora_br = datetime.now(fuso_br)

dt_hoje = agora_br.date()
dt_fim = dt_hoje + timedelta(days=7)

inicio_br = dt_hoje.strftime("%d/%m/%Y")
fim_br = dt_fim.strftime("%d/%m/%Y")

NTFY_TOPIC = "notificacoes_b3_carteira_completa" 

def enviar_ntfy(mensagem):
    url = f"https://ntfy.sh/{NTFY_TOPIC}"
    try:
        res = requests.post(url, data=mensagem.encode('utf-8'))
        print(f"Status NTFY: {res.status_code}")
    except Exception as e:
        print(f"Erro ao enviar ntfy: {e}")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://statusinvest.com.br/'
}

def extrair_ticker(evento):
    return str(
        evento.get("code") or 
        evento.get("ticker") or 
        evento.get("symbol") or 
        evento.get("companyName") or 
        "N/A"
    ).upper().strip()

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

def buscar_e_notificar():
    print(f"=== Varredura de Proventos B3 ({inicio_br} até {fim_br}) ===")
    
    # URL unificada com os parâmetros necessários
    url = f"https://statusinvest.com.br/acao/getevents?dateCom.start={inicio_br}&dateCom.end={fim_br}&byDateCom=true"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        print(f"Status da requisição: {response.status_code}")
        
        if response.status_code != 200:
            print("Não foi possível acessar a API de proventos.")
            return

        eventos = response.json()
        print(f"Total de eventos retornados na janela: {len(eventos)}")

        notificados = 0
        for ev in eventos:
            ticker = extrair_ticker(ev)
            
            # Checa os possíveis campos de Data COM
            data_com = converter_para_data(ev.get("dateCom") or ev.get("approvedOn") or ev.get("dateApproved"))
            
            # Checa os possíveis campos de Data de Pagamento
            data_pag = converter_para_data(ev.get("paymentDate"))
            
            tipo_nome, icone = identificar_tipo_provento(ev.get("earningType") or ev.get("type"))
            valor = ev.get("resultAbsoluteValue") or ev.get("value") or 0
            
            # 1. Checa Data COM no intervalo
            if data_com and dt_hoje <= data_com <= dt_fim:
                dias = (data_com - dt_hoje).days
                prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                
                msg = f"{prefixo} ({data_com.strftime('%d/%m/%Y')}) - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}"
                print(f"-> Disparando: {ticker} (Data COM: {data_com})")
                enviar_ntfy(msg)
                notificados += 1

            # 2. Checa Data de Pagamento no intervalo
            if data_pag and dt_hoje <= data_pag <= dt_fim:
                dias = (data_pag - dt_hoje).days
                prefixo = "✅ PAGAMENTO HOJE" if dias == 0 else ("🗓️ PAGAMENTO AMANHÃ" if dias == 1 else f"💰 PAGAMENTO EM {dias} DIAS")
                
                msg = f"{prefixo} ({data_pag.strftime('%d/%m/%Y')}) - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}"
                print(f"-> Disparando: {ticker} (Pagamento: {data_pag})")
                enviar_ntfy(msg)
                notificados += 1

        print(f"=== Varredura concluída. Total de notificações enviadas: {notificados} ===")

    except Exception as e:
        print(f"Erro durante a execução do script: {e}")

if __name__ == "__main__":
    buscar_e_notificar()
    
