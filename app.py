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
        res = requests.post(url, data=mensagem.encode('utf-8'), timeout=10)
        print(f"Status NTFY enviado: {res.status_code}")
    except Exception as e:
        print(f"Erro ao enviar ntfy: {e}")

# Lista de ações para monitoramento
TICKERS_B3 = [
    "VALE3.SA", "PETR4.SA", "ITSA4.SA", "BBAS3.SA", "BBDC4.SA",
    "ABEV3.SA", "TAEE11.SA", "EGIE3.SA", "CPLE6.SA", "VIVT3.SA",
    "KLBN11.SA", "SANB11.SA", "CXSE3.SA", "BBSE3.SA", "TRPL4.SA"
]

def processar_proventos():
    print(f"=== Varredura B3 via Yahoo Finance ({dt_hoje.strftime('%d/%m/%Y')} a {dt_fim.strftime('%d/%m/%Y')}) ===")
    notificados = 0

    for ticker_symbol in TICKERS_B3:
        ticker_clean = ticker_symbol.replace(".SA", "")
        try:
            ticker = yf.Ticker(ticker_symbol)

            # 1. Checagem do Calendário
            try:
                cal = ticker.calendar
                if cal is not None:
                    # Trata o retorno como dicionário ou DataFrame
                    ex_date = None
                    if isinstance(cal, dict) and "Ex-Dividend Date" in cal:
                        ex_date = cal["Ex-Dividend Date"]
                        if isinstance(ex_date, list) and len(ex_date) > 0:
                            ex_date = ex_date[0]
                    elif hasattr(cal, "get"):
                        ex_date = cal.get("Ex-Dividend Date")

                    if ex_date:
                        data_evt = ex_date.date() if hasattr(ex_date, 'date') else ex_date
                        if isinstance(data_evt, datetime):
                            data_evt = data_evt.date()

                        if dt_hoje <= data_evt <= dt_fim:
                            dias = (data_evt - dt_hoje).days
                            prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                            msg = f"{prefixo} ({data_evt.strftime('%d/%m/%Y')}) - {ticker_clean}\n💵 Tipo: Provento (Calendário)"
                            print(f"-> Disparando evento: {ticker_clean}")
                            enviar_ntfy(msg)
                            notificados += 1
            except Exception as err_cal:
                print(f"Aviso no calendário de {ticker_clean}: {err_cal}")

            # 2. Checagem dos Dividendos Recentes/Anunciados
            try:
                actions = ticker.actions
                if actions is not None and not actions.empty and "Dividends" in actions.columns:
                    divs = actions[actions["Dividends"] > 0]
                    for idx, row in divs.iterrows():
                        dt_div = idx.date() if hasattr(idx, 'date') else idx
                        if dt_hoje <= dt_div <= dt_fim:
                            valor = row["Dividends"]
                            dias = (dt_div - dt_hoje).days
                            prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                            msg = f"{prefixo} ({dt_div.strftime('%d/%m/%Y')}) - {ticker_clean}\n💵 Tipo: Provento\nValor: R$ {valor:.4f}"
                            print(f"-> Disparando dividendo: {ticker_clean}")
                            enviar_ntfy(msg)
                            notificados += 1
            except Exception as err_act:
                print(f"Aviso no histórico de {ticker_clean}: {err_act}")

        except Exception as e:
            print(f"Erro ao carregar dados de {ticker_symbol}: {e}")

    print(f"=== Varredura concluída. Total de notificações enviadas: {notificados} ===")

if __name__ == "__main__":
    processar_proventos()
    
