from datetime import datetime, timedelta
import zoneinfo
import requests
import yfinance as yf

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

# Lista de ações principais da B3 para monitoramento contínuo
TICKERS_B3 = [
    "VALE3.SA", "PETR4.SA", "ITSA4.SA", "BBAS3.SA", "BBDC4.SA",
    "ABEV3.SA", "TAEE11.SA", "EGIE3.SA", "CPLE6.SA", "VIVT3.SA",
    "KLBN11.SA", "SANB11.SA", "CXSE3.SA", "BBSE3.SA", "TRPL4.SA"
]

print(f"=== Varredura B3 via Yahoo Finance ({dt_hoje.strftime('%d/%m/%Y')} a {dt_fim.strftime('%d/%m/%Y')}) ===")

notificados = 0

for ticker_symbol in TICKERS_B3:
    try:
        ticker = yf.Ticker(ticker_symbol)
        ticker_clean = ticker_symbol.replace(".SA", "")
        
        # Obtém o calendário de eventos e dividendos do ativo
        calendar = ticker.calendar
        
        if calendar is not None and not calendar.empty:
            # Verifica datas de proventos/ex-date no calendário do Yahoo Finance
            for col in calendar.columns if hasattr(calendar, 'columns') else []:
                val = calendar[col].get("Ex-Dividend Date") or calendar[col].get("Dividend Date")
                if val:
                    data_evento = val.date() if hasattr(val, 'date') else None
                    if data_evento and dt_hoje <= data_evento <= dt_fim:
                        dias = (data_evento - dt_hoje).days
                        prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                        
                        msg = f"{prefixo} ({data_evento.strftime('%d/%m/%Y')}) - {ticker_clean}\n💵 Tipo: Provento (Dividendo/JCP)"
                        print(f"-> Disparando: {ticker_clean} ({data_evento})")
                        enviar_ntfy(msg)
                        notificados += 1

        # Checagem complementar do histórico recente de dividendos
        actions = ticker.actions
        if actions is not None and not actions.empty and "Dividends" in actions.columns:
            divs = actions[actions["Dividends"] > 0]
            for idx, row in divs.iterrows():
                dt_div = idx.date()
                if dt_hoje <= dt_div <= dt_fim:
                    valor = row["Dividends"]
                    dias = (dt_div - dt_hoje).days
                    prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                    
                    msg = f"{prefixo} ({dt_div.strftime('%d/%m/%Y')}) - {ticker_clean}\n💵 Tipo: Provento\nValor: R$ {valor:.4f}"
                    print(f"-> Disparando via histórico: {ticker_clean}")
                    enviar_ntfy(msg)
                    notificados += 1

    except Exception as e:
        print(f"Erro ao processar {ticker_symbol}: {e}")

print(f"=== Varredura concluída. Total de notificações enviadas: {notificados} ===")
