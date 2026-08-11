from datetime import datetime, timedelta
import zoneinfo
import requests

# 1. Configuração de Fuso Horário do Brasil
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
        print(f"Status NTFY enviado: {res.status_code}")
    except Exception as e:
        print(f"Erro ao enviar ntfy: {e}")

# Cabeçalho rotativo de navegador com cookies simulados
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Origin': 'https://statusinvest.com.br',
    'Referer': 'https://statusinvest.com.br/acoes/proventos'
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

def buscar_proventos():
    print(f"=== Varredura B3 ({inicio_br} a {fim_br}) ===")
    
    # Session para manter cookies e simular navegação humana
    session = requests.Session()
    session.headers.update(HEADERS)

    # 1. Tenta obter o cookie inicial acessando a home
    try:
        session.get("https://statusinvest.com.br/", timeout=10)
    except Exception:
        pass

    url = f"https://statusinvest.com.br/acao/getevents?dateCom.start={inicio_br}&dateCom.end={fim_br}&byDateCom=true"
    
    try:
        response = session.get(url, timeout=15)
        print(f"Status da resposta: {response.status_code}")

        if response.status_code == 200:
            eventos = response.json()
            print(f"Eventos retornados: {len(eventos)}")
            
            notificados = 0
            for ev in eventos:
                ticker = str(ev.get("code") or ev.get("ticker") or ev.get("companyName") or "").upper().strip()
                data_com = converter_para_data(ev.get("dateCom") or ev.get("approvedOn"))
                data_pag = converter_para_data(ev.get("paymentDate"))
                tipo_nome, icone = identificar_tipo_provento(ev.get("earningType"))
                valor = ev.get("resultAbsoluteValue", 0)

                # Notificação de Data COM
                if data_com and dt_hoje <= data_com <= dt_fim:
                    dias = (data_com - dt_hoje).days
                    prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                    msg = f"{prefixo} ({data_com.strftime('%d/%m/%Y')}) - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}"
                    print(f"-> Disparando: {ticker}")
                    enviar_ntfy(msg)
                    notificados += 1

                # Notificação de Pagamento
                if data_pag and dt_hoje <= data_pag <= dt_fim:
                    dias = (data_pag - dt_hoje).days
                    prefixo = "✅ PAGAMENTO HOJE" if dias == 0 else ("🗓️ PAGAMENTO AMANHÃ" if dias == 1 else f"💰 PAGAMENTO EM {dias} DIAS")
                    msg = f"{prefixo} ({data_pag.strftime('%d/%m/%Y')}) - {ticker}\n{icone} Tipo: {tipo_nome}\nValor: R$ {valor}"
                    print(f"-> Disparando Pagamento: {ticker}")
                    enviar_ntfy(msg)
                    notificados += 1

            print(f"=== Varredura concluída. Alertas disparados: {notificados} ===")
        else:
            print(f"API bloqueada com status {response.status_code}. Ativando modo de segurança.")

    except Exception as e:
        print(f"Erro na execução da requisição: {e}")

if __name__ == "__main__":
    buscar_proventos()
    
