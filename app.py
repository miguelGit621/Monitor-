from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração de Fuso Horário do Brasil
fuso_br = zoneinfo.ZoneInfo("America/Sao_Paulo")
agora_br = datetime.now(fuso_br)

dt_hoje = agora_br.date()
dt_fim = dt_hoje + timedelta(days=7) # Monitora até 7 dias no futuro

inicio_br = dt_hoje.strftime("%d/%m/%Y")
fim_br = dt_fim.strftime("%d/%m/%Y")

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

def extrair_ticker(evento):
    return str(
        evento.get("code") or 
        evento.get("ticker") or 
        evento.get("symbol") or 
        evento.get("companyName") or 
        "N/A"
    ).upper().strip()

def converter_para_data(data_str):
    if not data_str:
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
        return str(raw_tipo).capitalize(), "💰"

def obter_dy_str(evento):
    dy = evento.get("dy") or evento.get("dividendYield") or evento.get("yield")
    if dy is not None:
        try:
            return f"{float(dy):.2f}%"
        except (ValueError, TypeError):
            pass
    return "N/D"

print(f"=== Varredura Geral B3 ({inicio_br} até {fim_br}) ===")

# ==========================================
# 1. BUSCA DE DATAS COM (PRÓXIMOS 7 DIAS)
# ==========================================
url_com = f"https://statusinvest.com.br/acao/getevents?dateCom.start={inicio_br}&dateCom.end={fim_br}&byDateCom=true"

try:
    res = requests.get(url_com, headers=HEADERS, timeout=15)
    if res.status_code == 200:
        eventos = res.json()
        print(f"Eventos de Data COM localizados no período: {len(eventos)}")
        
        for ev in eventos:
            ticker = extrair_ticker(ev)
            data_com = converter_para_data(ev.get("dateCom") or ev.get("approvedOn"))
            
            tipo_nome, icone = identificar_tipo_provento(ev.get("earningType"))
            valor = ev.get("resultAbsoluteValue", 0)
            dy_str = obter_dy_str(ev)

            # Notifica qualquer evento que esteja no intervalo entre HOJE e os próximos 7 dias
            if data_com and dt_hoje <= data_com <= dt_fim:
                dias_restantes = (data_com - dt_hoje).days
                
                if dias_restantes == 0:
                    status_str = f"🚨 DATA COM HOJE ({data_com.strftime('%d/%m/%Y')})"
                elif dias_restantes == 1:
                    status_str = f"⚠️ DATA COM AMANHÃ ({data_com.strftime('%d/%m/%Y')})"
                else:
                    status_str = f"📅 DATA COM EM {dias_restantes} DIAS ({data_com.strftime('%d/%m/%Y')})"

                msg = f"{status_str} - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}\nDY: {dy_str}"
                print(f"-> NOTIFICANDO: {ticker} ({data_com.strftime('%d/%m/%Y')})")
                enviar_ntfy(msg)

except Exception as e:
    print(f"Erro no rastreamento de proventos: {e}")

# ==========================================
# 2. BUSCA DE PAGAMENTOS (PRÓXIMOS 7 DIAS)
# ==========================================
url_pag = f"https://statusinvest.com.br/acao/getevents?paymentDate.start={inicio_br}&paymentDate.end={fim_br}&byPaymentDate=true"

try:
    res_pag = requests.get(url_pag, headers=HEADERS, timeout=15)
    if res_pag.status_code == 200:
        eventos_pag = res_pag.json()
        
        for ev in eventos_pag:
            ticker = extrair_ticker(ev)
            data_pag = converter_para_data(ev.get("paymentDate"))
            
            tipo_nome, icone = identificar_tipo_provento(ev.get("earningType"))
            valor = ev.get("resultAbsoluteValue", 0)
            dy_str = obter_dy_str(ev)

            if data_pag and dt_hoje <= data_pag <= dt_fim:
                dias_restantes = (data_pag - dt_hoje).days
                
                if dias_restantes == 0:
                    status_str = f"✅ PAGAMENTO HOJE ({data_pag.strftime('%d/%m/%Y')})"
                elif dias_restantes == 1:
                    status_str = f"🗓️ PAGAMENTO AMANHÃ ({data_pag.strftime('%d/%m/%Y')})"
                else:
                    status_str = f"💰 PAGAMENTO EM {dias_restantes} DIAS ({data_pag.strftime('%d/%m/%Y')})"

                msg = f"{status_str} - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}\nDY: {dy_str}"
                print(f"-> NOTIFICANDO PAGAMENTO: {ticker} ({data_pag.strftime('%d/%m/%Y')})")
                enviar_ntfy(msg)

except Exception as e:
    print(f"Erro no rastreamento de pagamentos: {e}")

print("=== Varredura finalizada ===")
