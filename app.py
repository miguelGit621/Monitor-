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
    "A1MD34.SA", "A2MC34.SA", "AALR3.SA", "AAPL34.SA", "AAZQ11.SA", "ABBV34.SA",
    "ABCB4.SA", "ABCP11.SA", "ABEV3.SA", "ABTT34.SA", "ACCN34.SA", "ACNB34.SA",
    "ADBE34.SA", "ADPR34.SA", "ADSK34.SA", "AEXA34.SA", "AFGB34.SA", "AFHI11.SA",
    "AFOF11.SA", "AGRO3.SA", "AGRO34.SA", "AGXY3.SA", "AHEB3.SA", "AHEB4.SA",
    "AHEB6.SA", "AIEC11.SA", "AIGB34.SA", "AIRB34.SA", "AJFI11.SA", "AKAM34.SA",
    "ALMI11.SA", "ALOS3.SA", "ALPA4.SA", "ALUP11.SA", "ALUP3.SA", "ALZC11.SA",
    "ALZR11.SA", "AMAR3.SA", "AMAT34.SA", "AMBP3.SA", "AMED34.SA", "AMEI34.SA",
    "AMER3.SA", "AMGN34.SA", "AMPB34.SA", "AMXB34.SA", "AMZO34.SA", "ANAB34.SA",
    "ANCR11.SA", "ANEI3.SA", "ANSS34.SA", "ANTM34.SA", "AONB34.SA", "APAX34.SA",
    "APPL34.SA", "APTO11.SA", "ARCO34.SA", "ARCT11.SA", "ARML3.SA", "ARNC34.SA",
    "ARRI11.SA", "ARZZ3.SA", "ASAI3.SA", "ASIA11.SA", "ASML34.SA", "ASMT11.SA",
    "ATLP11.SA", "ATMP3.SA", "ATSA11.SA", "ATOO34.SA", "ATTV34.SA", "AURA33.SA",
    "AURE3.SA", "AURE4.SA", "AVGO34.SA", "AXP34.SA", "AZA11.SA", "AZEV3.SA",
    "AZEV4.SA", "AZUL4.SA", "AZZN34.SA", "B3SA3.SA", "B3ZA34.SA", "BABA34.SA",
    "BAHI3.SA", "BALM3.SA", "BALM4.SA", "BAPAR3.SA", "BARI11.SA", "BAXB34.SA",
    "BAZA3.SA", "BBYY34.SA", "BBAS3.SA", "BBFI11B.SA", "BBFO11.SA", "BBGO11.SA",
    "BBIG11.SA", "BBIM11.SA", "BBDC3.SA", "BBDC4.SA", "BBPO11.SA", "BBSE3.SA",
    "BBRC11.SA", "BBRK3.SA", "BCFF11.SA", "BCIA11.SA", "BCRI11.SA", "BCSC11.SA",
    "BDXB34.SA", "BDLL3.SA", "BDLL4.SA", "BDPB11.SA", "BEEF3.SA", "BEES3.SA",
    "BEES4.SA", "BENB34.SA", "BERK34.SA", "BFAIR11.SA", "BHOF11.SA", "BICE11.SA",
    "BIDI11.SA", "BIEF34.SA", "BIER11.SA", "BIIB34.SA", "BIVB34.SA", "BIZT11.SA",
    "BKBR3.SA", "BLAK34.SA", "BLAU3.SA", "BLAZ3.SA", "BLCA11.SA", "BLMC11.SA",
    "BLMG11.SA", "BLMO11.SA", "BMCB34.SA", "BMEB3.SA", "BMEB4.SA", "BMGB4.SA",
    "BMIN3.SA", "BMIN4.SA", "BMOB3.SA", "BMYB34.SA", "BNCB34.SA", "BNDX11.SA",
    "BNFS11.SA", "BNTX34.SA", "BNYB34.SA", "BOAC34.SA", "BOBR3.SA", "BOBR4.SA",
    "BOVA11.SA", "BPAC11.SA", "BPAN11.SA", "BPAN4.SA", "BPAR3.SA", "BPFF11.SA",
    "BPRP11.SA", "BRPP11.SA", "BRAP3.SA", "BRAP4.SA", "BRAX11.SA", "BRCO11.SA",
    "BRCR11.SA", "BRFS3.SA", "BRIV3.SA", "BRIV4.SA", "BRKM3.SA", "BRKM5.SA",
    "BREV11.SA", "BSBR34.SA", "BSLI3.SA", "BSLI4.SA", "BSYY34.SA", "BTAL11.SA",
    "BTLG11.SA", "BTSI11.SA", "CACR11.SA", "CAGB34.SA", "CALI3.SA", "CAMB3.SA",
    "CAML3.SA", "CARD3.SA", "CARE11.SA", "CARR34.SA", "CASH3.SA", "CATP34.SA",
    "CBEE3.SA", "CBOP11.SA", "CBRE34.SA", "CCHP34.SA", "CCME11.SA", "CCRO3.SA",
    "CCRE11.SA", "CDII11.SA", "CEDO3.SA", "CEDO4.SA", "CEEB3.SA", "CEEB5.SA",
    "CEED3.SA", "CEOC11.SA", "CEPE5.SA", "CEPE6.SA", "CEAB3.SA", "CEBR3.SA",
    "CEBR5.SA", "CEBR6.SA", "CGAS3.SA", "CGAS5.SA", "CGRA3.SA", "CGRA4.SA",
    "CHCJ11.SA", "CHKX34.SA", "CHLB34.SA", "CHVX34.SA", "CHINA11.SA", "CINF34.SA",
    "CJCT11.SA", "CLBC34.SA", "CLOR34.SA", "CLSA3.SA", "CLSC3.SA", "CLSC4.SA",
    "CMCS34.SA", "CMEG34.SA", "CMIG3.SA", "CMIG4.SA", "CMIN3.SA", "CMRE34.SA",
    "CNES11.SA", "COCA34.SA", "COCE3.SA", "COCE5.SA", "COGN3.SA", "COLG34.SA",
    "COST34.SA", "CPFE3.SA", "CPFF11.SA", "CPLE3.SA", "CPLE5.SA", "CPLE6.SA",
    "CPOF11.SA", "CPPG34.SA", "CPRH11.SA", "CPTI11.SA", "CPTR11.SA", "CPTS11.SA",
    "CPRE3.SA", "CRFB3.SA", "CRIV3.SA", "CRIV4.SA", "CRTE3.SA", "CSAN3.SA",
    "CSCO34.SA", "CSGP34.SA", "CSNA3.SA", "CSRN3.SA", "CSRN5.SA", "CSWH34.SA",
    "CSXB34.SA", "CTAS34.SA", "CTKA3.SA", "CTKA4.SA", "CTNM3.SA", "CTNM4.SA",
    "CTRP34.SA", "CTSA3.SA", "CTSA4.SA", "CTXT11.SA", "CTVA34.SA", "CURY3.SA",
    "CVCB3.SA", "CVSB34.SA", "CVSH34.SA", "CXAG11.SA", "CXCE11B.SA", "CXCI11.SA",
    "CXCO11.SA", "CXRI11.SA", "CXSE3.SA", "CYCR11.SA", "CYRE3.SA", "DEEC34.SA",
    "DESK3.SA", "DEVT11.SA", "DEXP3.SA", "DEXP4.SA", "DHER34.SA", "DIRR3.SA",
    "DISB34.SA", "DISN34.SA", "DIVO11.SA", "DLMT11.SA", "DLTR34.SA", "DMMO3.SA",
    "DMVF3.SA", "DODS3.SA", "DOTZ3.SA", "DRIT11B.SA", "DTCY3.SA", "DVFF11.SA",
    "DXCM34.SA", "EALT3.SA", "EALT4.SA", "EAAB34.SA", "EBAY34.SA", "ECEB3.SA",
    "ECEB5.SA", "ECEB6.SA", "ECEF11.SA", "ECOR3.SA", "ECOO11.SA", "EDGA11.SA",
    "EDFO11.SA", "EGIE3.SA", "EKTR3.SA", "ELAX11.SA", "ELDO11.SA", "ELEK3.SA",
    "ELEK4.SA", "ELET3.SA", "ELET5.SA", "ELET6.SA", "EMBR3.SA", "ENBR3.SA",
    "ENEV3.SA", "ENGI11.SA", "ENGI3.SA", "ENGI4.SA", "EQIX34.SA", "EQMA3B.SA",
    "EQPA3.SA", "EQPA7.SA", "EQTL3.SA", "ERCR11.SA", "ERIX34.SA", "ERPA11.SA",
    "ESGB11.SA", "ESPA3.SA", "ESSO34.SA", "ESTR4.SA", "ETER3.SA", "ETYB34.SA",
    "EUCA3.SA", "EUCA4.SA", "EURO11.SA", "EVBI11.SA", "EVEN3.SA", "EXPE34.SA",
    "EXXO34.SA", "EZTC3.SA", "FAED11.SA", "FAMB11B.SA", "FAST34.SA", "FCFL11.SA",
    "FCSL11.SA", "FDMO34.SA", "FDXB34.SA", "FESA4.SA", "FESC11.SA", "FEXC11.SA",
    "FGAA11.SA", "FHER3.SA", "FIGS11.SA", "FIIB11.SA", "FIIP11B.SA", "FIND11.SA",
    "FINF11.SA", "FIQE3.SA", "FIPV11B.SA", "FIXA11.SA", "FIXX11.SA", "FLMA11.SA",
    "FLRP11.SA", "FLRY3.SA", "FMOF11.SA", "FOXB34.SA", "FPAB11.SA", "FRAS3.SA",
    "FRTA3.SA", "FSLR34.SA", "FSTU11.SA", "FTNT34.SA", "FVPQ11.SA", "GALG11.SA",
    "GAME11.SA", "GARE11.SA", "GCFF11.SA", "GCRA11.SA", "GEFC34.SA", "GENO11.SA",
    "GEPA3.SA", "GEPA34.SA", "GFSA3.SA", "GGBR4.SA", "GGRC11.SA", "GILD34.SA",
    "GMAT3.SA", "GOGL34.SA", "GOAU4.SA", "GOLD11.SA", "GOLL4.SA", "GOVE11.SA",
    "GPLN3.SA", "GSFI11.SA", "GSGI34.SA", "GTWR11.SA", "GUAR3.SA", "GUAR4.SA",
    "HABT11.SA", "HAGA3.SA", "HAGA4.SA", "HALI34.SA", "HAPV3.SA", "HASB34.SA",
    "HASH11.SA", "HBOR3.SA", "HBRE3.SA", "HBRH11.SA", "HCHG11.SA", "HCTR11.SA",
    "HETA3.SA", "HETA4.SA", "FEXC11.SA", "HGAG11.SA", "HGBL11.SA", "HGBS11.SA",
    "HGCR11.SA", "HGFF11.SA", "HGLG11.SA", "HGPO11.SA", "HGRE11.SA", "HGRU11.SA",
    "HIGB34.SA", "HOLX34.SA", "HOME34.SA", "HONB34.SA", "HOOT4.SA", "HPOF11.SA",
    "HPPO11.SA", "HPQB34.SA", "HREC11.SA", "HSML11.SA", "HSTC34.SA", "HTMX11.SA",
    "HUMA34.SA", "HYPE3.SA", "IBOB11.SA", "IBMG34.SA", "IDXX34.SA", "IFCM3.SA",
    "ILMN34.SA", "INBR32.SA", "INCY34.SA", "INFO34.SA", "INTB3.SA", "INTC34.SA",
    "INTU34.SA", "IPGA34.SA", "IRBR3.SA", "IRDM11.SA", "ISRG34.SA", "ISUS11.SA",
    "ITSA3.SA", "ITSA4.SA", "ITUB3.SA", "ITUB4.SA", "ITUB34.SA", "IVVB11.SA",
    "JALL3.SA", "JBHT34.SA", "JBDU4.SA", "JCIb34.SA", "JBSS3.SA", "JHSF3.SA",
    "JNJB34.SA", "JOPA3.SA", "JOPA4.SA", "JPMC34.SA", "JSRE11.SA", "KCHB34.SA",
    "KCRE11.SA", "KEFAR11.SA", "KEPL3.SA", "KEYB34.SA", "KEYS34.SA", "KINP11.SA",
    "KISU11.SA", "KLAC34.SA", "KLBN11.SA", "KLBN3.SA", "KMBB34.SA", "KNCF11.SA",
    "KNCA11.SA", "KNCR11.SA", "KNSC11.SA", "KOCH34.SA", "KRCO34.SA", "KRSA3.SA",
    "LAND3.SA", "LAVV3.SA", "LEVE3.SA", "LIGH3.SA", "LIGT3.SA", "LIGT4.SA", "LIF11.SA",
    "LIPR3.SA", "LIXC3.SA", "LIXC4.SA", "LLYY34.SA", "LMTB34.SA", "LOGG3.SA",
    "LOGN3.SA", "LREN3.SA", "LRCX34.SA", "LUGG11.SA", "LULU34.SA", "LUPA3.SA",
    "LUXA4.SA", "LVBI11.SA", "LVTC3.SA", "LWSA3.SA", "M1TA34.SA", "MALT4.SA",
    "MALL11.SA", "MANA11.SA", "MAPT3.SA", "MAPT4.SA", "MARB34.SA", "MATB11.SA",
    "MATD3.SA", "MAXR11.SA", "MCDO34.SA", "MCHC34.SA", "MCHF11.SA", "MCKE34.SA",
    "MCOB34.SA", "MDTZ34.SA", "MDNE3.SA", "MDLZ34.SA", "MEAL3.SA", "MELI34.SA",
    "MELK3.SA", "META34.SA", "METB34.SA", "MFII11.SA", "MGLU3.SA", "MCHP34.SA",
    "MILS3.SA", "MITRE3.SA", "MMMD34.SA", "MNPR3.SA", "MNST34.SA", "MOAR3.SA",
    "MODL3.SA", "MORE11.SA", "MOVI3.SA", "MOOO34.SA", "MPCI34.SA", "MRFG3.SA",
    "MRNA34.SA", "MRVE3.SA", "MSCD34.SA", "MSFT34.SA", "MSCI34.SA", "MTCB34.SA",
    "MULT3.SA", "MWET3.SA", "MWET4.SA", "MXRF11.SA", "MYPK3.SA", "NASD11.SA",
    "NAVI34.SA", "NAVT11.SA", "NDAQ34.SA", "NEOE3.SA", "NEER34.SA", "NGRD3.SA",
    "NEWL11.SA", "NKEG34.SA", "NOCG34.SA", "NORD3.SA", "NORD4.SA", "NSCG34.SA",
    "NSLU11.SA", "NTAP34.SA", "NTCO3.SA", "NTRS34.SA", "NUBR33.SA", "NUTR3.SA",
    "NVDC34.SA", "NVDA34.SA", "NVHO11.SA", "NVTG34.SA", "NVOO34.SA", "NWSA34.SA",
    "NXPI34.SA", "OBRD3.SA", "ODFL34.SA", "OMCB34.SA", "ONEF11.SA", "ONON34.SA",
    "ORCL34.SA", "ORLY34.SA", "ORVR3.SA", "OSXB3.SA", "OTIS34.SA", "OUJP11.SA",
    "OULG11.SA", "PARD3.SA", "PATC11.SA", "PATI3.SA", "PATI4.SA", "PAYX34.SA",
    "PCAR3.SA", "PCAR34.SA", "PDGR3.SA", "PEGp34.SA", "PEPB34.SA", "PETR3.SA",
    "PETR4.SA", "PFIZ34.SA", "PGCO34.SA", "PGMN3.SA", "PGPB34.SA", "PIBB11.SA",
    "PINE3.SA", "PINE4.SA", "PLAS3.SA", "PLCR11.SA", "PLPL3.SA", "PNCB34.SA",
    "PNVL3.SA", "POMO4.SA", "PORD11.SA", "PORT3.SA", "POSI3.SA", "PPGM34.SA", "PQAG11.SA",
    "PQDP11.SA", "PRIO3.SA", "PRNR3.SA", "PRTS11.SA", "PRVU34.SA", "PSAE34.SA",
    "PSSA3.SA", "PSXG34.SA", "PTBL3.SA", "PTNT3.SA", "PTNT4.SA", "PVBI11.SA",
    "PWRB34.SA", "PYPL34.SA", "QCOM34.SA", "QUAL3.SA", "RADL3.SA", "RAIZ4.SA",
    "RANI3.SA", "RAPT3.SA", "RAPT4.SA", "RBDS11.SA", "RBED11.SA", "RBHY11.SA",
    "RBRP11.SA", "RBRR11.SA", "RBRY11.SA", "RBVA11.SA", "RBLG11.SA", "RDES11.SA",
    "RDNI3.SA", "RDOR3.SA", "RDPG11.SA", "REC11.SA", "RECIP11.SA", "RECR11.SA",
    "RECT11.SA", "RECRAFT.SA", "REGN34.SA", "RENE3.SA", "RENE4.SA", "RENT3.SA",
    "RNDP11.SA", "RNEW3.SA", "RNEW4.SA", "ROMI3.SA", "ROST34.SA", "RPAD3.SA",
    "RRPX3.SA", "RRPX4.SA", "RSID3.SA", "RSUL4.SA", "RTXB34.SA", "RUM3.SA",
    "RURA11.SA", "RZAK11.SA", "RZAT11.SA", "RZTR11.SA", "SAAG11.SA", "SANB11.SA",
    "SANB3.SA", "SANB4.SA", "SAPB11.SA", "SAPR3.SA", "SAPR4.SA", "SARE11.SA",
    "SBAC34.SA", "SBFG3.SA", "SBPO11.SA", "SBSP3.SA", "SBUB34.SA", "SCAR3.SA",
    "SCHW34.SA", "SDIL11.SA", "SEQL3.SA", "SESP3.SA", "SHPH11.SA", "SHUL3.SA",
    "SHUL4.SA", "SHWG34.SA", "SIFI34.SA", "SIMH3.SA", "SIRI34.SA", "SLCE3.SA",
    "SLED3.SA", "SLED4.SA", "SMAL11.SA", "SMTO3.SA", "SNAG11.SA", "SNCI11.SA",
    "SOJA3.SA", "SOND3.SA", "SOND4.SA", "SPGI34.SA", "SPXB11.SA", "SPXI11.SA", "SPVJ11.SA",
    "SPTW11.SA", "SRNA3.SA", "STBP3.SA", "SUZB3.SA", "SWKS34.SA", "SYK34.SA",
    "SYNE3.SA", "SYNE4.SA", "T1OM34.SA", "TAEE11.SA", "TAEE3.SA", "TAEE4.SA",
    "TASA3.SA", "TASA4.SA", "TECK11.SA", "TEKA3.SA", "TEKA4.SA", "TECN3.SA",
    "TELB3.SA", "TELB4.SA", "TEND3.SA", "TFCB34.SA", "TFCV3.SA", "TFCO4.SA",
    "TGAR11.SA", "TGMA3.SA", "TIMS3.SA", "TISC3.SA", "TORD11.SA", "TOTS3.SA",
    "TOTVS3.SA", "TPIS3.SA", "TRAD3.SA", "TRIS3.SA", "TRNT11.SA", "TRPL3.SA",
    "TRPL4.SA", "TROW34.SA", "TRVG34.SA", "TRXF11.SA", "TSCO34.SA", "TSLA34.SA",
    "TUPY3.SA", "TTEN3.SA", "TXN34.SA", "TXRX3.SA", "TXRX4.SA", "UGPA3.SA",
    "UNHH34.SA", "UNIP3.SA", "UNIP4.SA", "UNIP5.SA", "UNIP6.SA", "UNP34.SA",
    "UPSI34.SA", "URPR11.SA", "USIM3.SA", "USIM5.SA", "USTK11.SA", "VALE3.SA",
    "VAMO3.SA", "VBBR3.SA", "VCRA11.SA", "VGIA11.SA", "VGIP11.SA", "VGIR11.SA",
    "VGHT11.SA", "VILG11.SA", "VINO11.SA", "VISA34.SA", "VISC11.SA", "VIVT3.SA",
    "VIVA3.SA", "VIVR3.SA", "VLID3.SA", "VLOL11.SA", "VRTX34.SA", "VSLH11.SA",
    "VSPT3.SA", "VTLT11.SA", "VZZA34.SA", "WBAO34.SA", "WDCB34.SA", "WEGE3.SA",
    "WEST3.SA", "WFCB34.SA", "WHGR11.SA", "WHRL3.SA", "WHRL4.SA", "WIZC3.SA",
    "WLMM3.SA", "WLMM4.SA", "WMBR34.SA", "WMTB34.SA", "WSTB34.SA", "WTSP11.SA",
    "XINA11.SA", "XMAL11.SA", "XPIN11.SA", "XPLG11.SA", "XPML11.SA", "XPSF11.SA",
]

def processar_proventos():
    print(f"=== Varredura B3 com Preço e Provento ({dt_hoje.strftime('%d/%m/%Y')} a {dt_fim.strftime('%d/%m/%Y')}) ===")
    notificados = 0

    for ticker_symbol in TICKERS_B3:
        ticker_clean = ticker_symbol.replace(".SA", "")
        try:
            ticker = yf.Ticker(ticker_symbol)

            # Obtém a cotação atual de mercado da ação
            preco_atual = None
            try:
                # Tenta pegar pelo histórico recente ou info rápida
                todays_data = ticker.history(period="1d")
                if not todays_data.empty:
                    preco_atual = float(todays_data["Close"].iloc[-1])
                else:
                    info = ticker.info
                    preco_atual = float(info.get("currentPrice") or info.get("regularMarketPrice") or 0)
            except Exception:
                pass

            preco_str = f"R$ {preco_atual:.2f}" if preco_atual and preco_atual > 0 else "N/D"

            # 1. Checagem do Calendário
            try:
                cal = ticker.calendar
                if cal is not None:
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
                            msg = f"{prefixo} ({data_evt.strftime('%d/%m/%Y')}) - {ticker_clean}\n💵 Tipo: Provento (Calendário)\n📈 Cotação Atual: {preco_str}"
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
                            
                            # Cálculo da porcentagem do provento em relação ao preço atual (Yield do evento)
                            if preco_atual and preco_atual > 0:
                                percentual_dy = (valor / preco_atual) * 100
                                yield_str = f"{percentual_dy:.2f}%"
                            else:
                                yield_str = "N/D"

                            dias = (dt_div - dt_hoje).days
                            prefixo = "🚨 DATA COM HOJE" if dias == 0 else ("⚠️ DATA COM AMANHÃ" if dias == 1 else f"📅 DATA COM EM {dias} DIAS")
                            
                            msg = (
                                f"{prefixo} ({dt_div.strftime('%d/%m/%Y')}) - {ticker_clean}\n"
                                f"💵 Valor do Provento: R$ {valor:.4f}\n"
                                f"📈 Cotação Atual: {preco_str}\n"
                                f"📊 Yield do Evento: {yield_str}"
                            )
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
    
