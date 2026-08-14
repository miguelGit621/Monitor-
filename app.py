import os
import requests
import pandas as pd

TICKERS_ACOES = [
    "A1MD34.SA", "A2MC34.SA", "AALR3.SA", "AAPL34.SA", "ABBV34.SA", "ABCB4.SA", "ABEV3.SA", "ABTT34.SA", "ACCN34.SA", "ACNB34.SA", "ADBE34.SA", "ADPR34.SA", "ADSK34.SA", "AEXA34.SA", "AFGB34.SA", "AGRO3.SA", "AGRO34.SA", "AGXY3.SA", "AHEB3.SA", "AHEB4.SA", "AHEB6.SA", "AIGB34.SA", "AIRB34.SA", "AKAM34.SA", "ALOS3.SA", "ALPA4.SA", "ALUP3.SA", "ALUP4.SA", "AMAR3.SA", "AMAT34.SA", "AMBP3.SA", "AMED34.SA", "AMEI34.SA", "AMER3.SA", "AMGN34.SA", "AMPB34.SA", "AMXB34.SA", "AMZO34.SA", "ANAB34.SA", "ANSS34.SA", "ANTM34.SA", "AONB34.SA", "APAX34.SA", "ARCO34.SA", "ARML3.SA", "ARNC34.SA", "ARZZ3.SA", "ASAI3.SA", "ASML34.SA", "ATOO34.SA", "ATTV34.SA", "AURA33.SA", "AURE3.SA", "AURE4.SA", "AVGO34.SA", "AXP34.SA", "AZEV3.SA", "AZEV4.SA", "AZUL4.SA", "AZZN34.SA", "B3SA3.SA", "B3ZA34.SA", "BABA34.SA", "BAHI3.SA", "BALM3.SA", "BALM4.SA", "BAXB34.SA", "BAZA3.SA", "BBYY34.SA", "BBAS3.SA", "BBDC3.SA", "BBDC4.SA", "BBSE3.SA", "BDXB34.SA", "BDLL3.SA", "BDLL4.SA", "BEEF3.SA", "BEES3.SA", "BEES4.SA", "BENB34.SA", "BERK34.SA", "BIEF34.SA", "BIER11.SA", "BIIB34.SA", "BIVB34.SA", "BLAK34.SA", "BLAU3.SA", "BLAZ3.SA", "BMEB3.SA", "BMEB4.SA", "BMGB4.SA", "BMIN3.SA", "BMIN4.SA", "BMOB3.SA", "BMYB34.SA", "BNCB34.SA", "BNTX34.SA", "BNYB34.SA", "BOAC34.SA", "BOBR3.SA", "BOBR4.SA", "BPAN4.SA", "BPAR3.SA", "BRAP3.SA", "BRAP4.SA", "BRFS3.SA", "BRIV3.SA", "BRIV4.SA", "BRKM3.SA", "BRKM5.SA", "BSBR34.SA", "BSLI3.SA", "BSLI4.SA", "BSYY34.SA", "CAGB34.SA", "CALI3.SA", "CAMB3.SA", "CAML3.SA", "CARD3.SA", "CARR34.SA", "CASH3.SA", "CATP34.SA", "CBEE3.SA", "CBRE34.SA", "CCHP34.SA", "CCRO3.SA", "CEDO3.SA", "CEDO4.SA", "CEEB3.SA", "CEEB5.SA", "CEED3.SA", "CEPE5.SA", "CEPE6.SA", "CEAB3.SA", "CEBR3.SA", "CEBR5.SA", "CEBR6.SA", "CGAS3.SA", "CGAS5.SA", "CGRA3.SA", "CGRA4.SA", "CHKX34.SA", "CHLB34.SA", "CHVX34.SA", "CINF34.SA", "CLBC34.SA", "CLOR34.SA", "CLSA3.SA", "CLSC3.SA", "CLSC4.SA", "CMCS34.SA", "CMEG34.SA", "CMIG3.SA", "CMIG4.SA", "CMIN3.SA", "CMRE34.SA", "COCA34.SA", "COCE3.SA", "COCE5.SA", "COGN3.SA", "COLG34.SA", "COST34.SA", "CPFE3.SA", "CPLE3.SA", "CPLE5.SA", "CPLE6.SA", "CPPG34.SA", "CPRE3.SA", "CRFB3.SA", "CRIV3.SA", "CRIV4.SA", "CRTE3.SA", "CSAN3.SA", "CSCO34.SA", "CSGP34.SA", "CSNA3.SA", "CSRN3.SA", "CSRN5.SA", "CSWH34.SA", "CSXB34.SA", "CTAS34.SA", "CTKA3.SA", "CTKA4.SA", "CTNM3.SA", "CTNM4.SA", "CTRP34.SA", "CTSA3.SA", "CTSA4.SA", "CTVA34.SA", "CURY3.SA", "CVCB3.SA", "CVSB34.SA", "CVSH34.SA", "CYRE3.SA", "DEEC34.SA", "DESK3.SA", "DEXP3.SA", "DEXP4.SA", "DHER34.SA", "DIRR3.SA", "DISB34.SA", "DISN34.SA", "DLTR34.SA", "DMVF3.SA", "DODS3.SA", "DOTZ3.SA", "DTCY3.SA", "DXCM34.SA", "EALT3.SA", "EALT4.SA", "EAAB34.SA", "EBAY34.SA", "ECEB3.SA", "ECEB5.SA", "ECEB6.SA", "ECOR3.SA", "EGIE3.SA", "EKTR3.SA", "ELEK3.SA", "ELEK4.SA", "ELET3.SA", "ELET5.SA", "ELET6.SA", "EMBR3.SA", "ENEV3.SA", "ENGI3.SA", "ENGI4.SA", "EQIX34.SA", "EQMA3B.SA", "EQPA3.SA", "EQPA7.SA", "EQTL3.SA", "ERIX34.SA", "ESPA3.SA", "ESSO34.SA", "ESTR4.SA", "ETER3.SA", "ETYB34.SA", "EUCA3.SA", "EUCA4.SA", "EVEN3.SA", "EXPE34.SA", "EXXO34.SA", "EZTC3.SA", "FAST34.SA", "FESA4.SA", "FHER3.SA", "FIQE3.SA", "FLRY3.SA", "FOXB34.SA", "FRAS3.SA", "FRTA3.SA", "FSLR34.SA", "FTNT34.SA", "GEFC34.SA", "GEPA3.SA", "GEPA34.SA", "GFSA3.SA", "GGBR4.SA", "GILD34.SA", "GMAT3.SA", "GOAU4.SA", "GOOGL34.SA", "GOLL4.SA", "GPLN3.SA", "GSGI34.SA", "GUAR3.SA", "GUAR4.SA", "HAGA3.SA", "HAGA4.SA", "HALI34.SA", "HAPV3.SA", "HASB34.SA", "HBOR3.SA", "HBRE3.SA", "HETA3.SA", "HETA4.SA", "HIGB34.SA", "HOLX34.SA", "HOME34.SA", "HONB34.SA", "HOOT4.SA", "HPQB34.SA", "HSTC34.SA", "HUMA34.SA", "HYPE3.SA", "IBMG34.SA", "IDXX34.SA", "IFCM3.SA", "ILMN34.SA", "INBR32.SA", "INCY34.SA", "INFO34.SA", "INTB3.SA", "INTC34.SA", "INTU34.SA", "IPGA34.SA", "IRBR3.SA", "ISRG34.SA", "ITSA3.SA", "ITSA4.SA", "ITUB3.SA", "ITUB4.SA", "ITUB34.SA", "JALL3.SA", "JBHT34.SA", "JBDU4.SA", "JBSS3.SA", "JHSF3.SA", "JNJB34.SA", "JOPA3.SA", "JOPA4.SA", "JPMC34.SA", "KCHB34.SA", "KEPL3.SA", "KEYB34.SA", "KEYS34.SA", "KLAC34.SA", "KLBN3.SA", "KMBB34.SA", "KOCH34.SA", "KRCO34.SA", "KRSA3.SA", "LAND3.SA", "LAVV3.SA", "LEVE3.SA", "LIGH3.SA", "LIGT3.SA", "LIGT4.SA", "LIPR3.SA", "LIXC3.SA", "LIXC4.SA", "LLYY34.SA", "LMTB34.SA", "LOGG3.SA", "LOGN3.SA", "LREN3.SA", "LRCX34.SA", "LULU34.SA", "LUPA3.SA", "LUXA4.SA", "LVTC3.SA", "LWSA3.SA", "MALT4.SA", "MAPT3.SA", "MAPT4.SA", "MARB34.SA", "MATD3.SA", "MCDO34.SA", "MCHC34.SA", "MCKE34.SA", "MCOB34.SA", "MDTZ34.SA", "MDNE3.SA", "MDLZ34.SA", "MEAL3.SA", "MELI34.SA", "MELK3.SA", "META34.SA", "METB34.SA", "MGLU3.SA", "MCHP34.SA", "MILS3.SA", "MITRE3.SA", "MMMD34.SA", "MNPR3.SA", "MNST34.SA", "MOAR3.SA", "MODL3.SA", "MOVI3.SA", "MOOO34.SA", "MPCI34.SA", "MRFG3.SA", "MRNA34.SA", "MRVE3.SA", "MSCD34.SA", "MSFT34.SA", "MSCI34.SA", "MTCB34.SA", "MULT3.SA", "MWET3.SA", "MWET4.SA", "MYPK3.SA", "NAVI34.SA", "NDAQ34.SA", "NEOE3.SA", "NEER34.SA", "NGRD3.SA", "NKEG34.SA", "NOCG34.SA", "NORD3.SA", "NORD4.SA", "NSCG34.SA", "NTAP34.SA", "NTCO3.SA", "NTRS34.SA", "NUTR3.SA", "NVDA34.SA", "NVTG34.SA", "NVOO34.SA", "NWSA34.SA", "NXPI34.SA", "OBRD3.SA", "ODFL34.SA", "OMCB34.SA", "ONON34.SA", "ORCL34.SA", "ORLY34.SA", "ORVR3.SA", "OSXB3.SA", "OTIS34.SA", "PARD3.SA", "PATI3.SA", "PATI4.SA", "PAYX34.SA", "PCAR3.SA", "PDGR3.SA", "PEPB34.SA", "PETR3.SA", "PETR4.SA", "PFIZ34.SA", "PGCO34.SA", "PGMN3.SA", "PGPB34.SA", "PINE3.SA", "PINE4.SA", "PLAS3.SA", "PLPL3.SA", "PNCB34.SA", "PNVL3.SA", "POMO4.SA", "PORT3.SA", "POSI3.SA", "PPGM34.SA", "PRIO3.SA", "PRNR3.SA", "PRVU34.SA", "PSAE34.SA", "PSSA3.SA", "PSXG34.SA", "PTBL3.SA", "PTNT3.SA", "PTNT4.SA", "PWRB34.SA", "PYPL34.SA", "QCOM34.SA", "QUAL3.SA", "RADL3.SA", "RAIL3.SA", "RAIZ4.SA", "RANI3.SA", "RAPT3.SA", "RAPT4.SA", "RDNI3.SA", "RDOR3.SA", "REGN34.SA", "RENE3.SA", "RENE4.SA", "RENT3.SA", "RNEW3.SA", "RNEW4.SA", "ROMI3.SA", "ROST34.SA", "ROXO34.SA", "RPAD3.SA", "RRPX3.SA", "RRPX4.SA", "RSID3.SA", "RSUL4.SA", "RTXB34.SA", "SANB3.SA", "SANB4.SA", "SAPR3.SA", "SAPR4.SA", "SBAC34.SA", "SBFG3.SA", "SBSP3.SA", "SBUB34.SA", "SCAR3.SA", "SCHW34.SA", "SEQL3.SA", "SESP3.SA", "SHUL3.SA", "SHUL4.SA", "SHWG34.SA", "SIFI34.SA", "SIMH3.SA", "SIRI34.SA", "SLCE3.SA", "SMTO3.SA", "SOJA3.SA", "SOND3.SA", "SOND4.SA", "SPGI34.SA", "SRNA3.SA", "STBP3.SA", "SUZB3.SA", "SWKS34.SA", "SYK34.SA", "SYNE3.SA", "SYNE4.SA", "T1OM34.SA", "TAEE3.SA", "TAEE4.SA", "TASA3.SA", "TASA4.SA", "TEKA3.SA", "TEKA4.SA", "TECN3.SA", "TELB3.SA", "TELB4.SA", "TEND3.SA", "TFCB34.SA", "TFCV3.SA", "TFCO4.SA", "TGMA3.SA", "TIMS3.SA", "TISC3.SA", "TOTVS3.SA", "TPIS3.SA", "TRAD3.SA", "TRIS3.SA", "TRPL3.SA", "TRPL4.SA", "TROW34.SA", "TRVG34.SA", "TSCO34.SA", "TSLA34.SA", "TUPY3.SA", "TTEN3.SA", "TXN34.SA", "TXRX3.SA", "TXRX4.SA", "UGPA3.SA", "UNHH34.SA", "UNIP3.SA", "UNIP4.SA", "UNIP5.SA", "UNIP6.SA", "UNP34.SA", "UPSI34.SA", "USIM3.SA", "USIM5.SA", "VALE3.SA", "VAMO3.SA", "VBBR3.SA", "VISA34.SA", "VIVT3.SA", "VIVA3.SA", "VIVR3.SA", "VLID3.SA", "VRTX34.SA", "VSPT3.SA", "VZZA34.SA", "WBAO34.SA", "WDCB34.SA", "WEGE3.SA", "WEST3.SA", "WFCB34.SA", "WHRL3.SA", "WHRL4.SA", "WIZC3.SA", "WLMM3.SA", "WLMM4.SA", "WMBR34.SA", "WMTB34.SA", "WSTB34.SA", "ZAMP3.SA"
]

TICKERS_FIIS = [
    "AAZQ11.SA", "ABCP11.SA", "AFHI11.SA", "AFOF11.SA", "AIEC11.SA", "AJFI11.SA", "ALMI11.SA", "ALUP11.SA", "ALZC11.SA", "ALZR11.SA", "ANCR11.SA", "ANEI3.SA", "APTO11.SA", "ARCT11.SA", "ARRI11.SA", "ASIA11.SA", "ASMT11.SA", "ATLP11.SA", "ATSA11.SA", "AZA11.SA", "BARI11.SA", "BBFI11B.SA", "BBFO11.SA", "BBGO11.SA", "BBIG11.SA", "BBIM11.SA", "BBPO11.SA", "BBRC11.SA", "BCIA11.SA", "BCRI11.SA", "BCSC11.SA", "BDPB11.SA", "BFAIR11.SA", "BHOF11.SA", "BICE11.SA", "BIZT11.SA", "BLCA11.SA", "BLMC11.SA", "BLMG11.SA", "BLMO11.SA", "BNDX11.SA", "BNFS11.SA", "BOVA11.SA", "BPAC11.SA", "BPAN11.SA", "BPFF11.SA", "BPRP11.SA", "BRPP11.SA", "BRAX11.SA", "BRCO11.SA", "BRCR11.SA", "BREV11.SA", "BTAL11.SA", "BTLG11.SA", "BTSI11.SA", "CACR11.SA", "CARE11.SA", "CBOP11.SA", "CCME11.SA", "CCRE11.SA", "CDII11.SA", "CEOC11.SA", "CHCJ11.SA", "CHINA11.SA", "CJCT11.SA", "CNES11.SA", "CPFF11.SA", "CPOF11.SA", "CPRH11.SA", "CPTI11.SA", "CPTR11.SA", "CPTS11.SA", "CTXT11.SA", "CXAG11.SA", "CXCE11B.SA", "CXCI11.SA", "CXCO11.SA", "CXRI11.SA", "CXSE3.SA", "CYCR11.SA", "DEVT11.SA", "DIVO11.SA", "DLMT11.SA", "DRIT11B.SA", "DVFF11.SA", "ECEF11.SA", "ECOO11.SA", "EDGA11.SA", "EDFO11.SA", "ELAX11.SA", "ELDO11.SA", "ENGI11.SA", "ERCR11.SA", "ERPA11.SA", "ESGB11.SA", "EURO11.SA", "EVBI11.SA", "FAED11.SA", "FAMB11B.SA", "FCFL11.SA", "FCSL11.SA", "FESC11.SA", "FEXC11.SA", "FGAA11.SA", "FIGS11.SA", "FIIB11.SA", "FIIP11B.SA", "FIND11.SA", "FINF11.SA", "FIPV11B.SA", "FIXA11.SA", "FIXX11.SA", "FLMA11.SA", "FLRP11.SA", "FMOF11.SA", "FPAB11.SA", "FSTU11.SA", "FVPQ11.SA", "GAME11.SA", "GARE11.SA", "GCFF11.SA", "GCRA11.SA", "GENO11.SA", "GGRC11.SA", "GOLD11.SA", "GOVE11.SA", "GSFI11.SA", "GTWR11.SA", "HABT11.SA", "HASH11.SA", "HBRH11.SA", "HCHG11.SA", "HCTR11.SA", "HGAG11.SA", "HGBL11.SA", "HGBS11.SA", "HGCR11.SA", "HGFF11.SA", "HGLG11.SA", "HGPO11.SA", "HGRE11.SA", "HGRU11.SA", "HPOF11.SA", "HPPO11.SA", "HREC11.SA", "HSML11.SA", "HTMX11.SA", "IBOB11.SA", "IRDM11.SA", "ISUS11.SA", "IVVB11.SA", "JSRE11.SA", "KCRE11.SA", "KEFAR11.SA", "KINP11.SA", "KISU11.SA", "KLBN11.SA", "KNCF11.SA", "KNCA11.SA", "KNCR11.SA", "KNSC11.SA", "LIF11.SA", "LUGG11.SA", "LVBI11.SA", "MALL11.SA", "MANA11.SA", "MATB11.SA", "MAXR11.SA", "MCHF11.SA", "MFII11.SA", "MORE11.SA", "MXRF11.SA", "NASD11.SA", "NAVT11.SA", "NEWL11.SA", "NSLU11.SA", "NVHO11.SA", "ONEF11.SA", "OUJP11.SA", "OULG11.SA", "PATC11.SA", "PIBB11.SA", "PLCR11.SA", "PORD11.SA", "PQAG11.SA", "PQDP11.SA", "PRTS11.SA", "PVBI11.SA", "RBDS11.SA", "RBED11.SA", "RBHY11.SA", "RBRP11.SA", "RBRR11.SA", "RBRY11.SA", "RBVA11.SA", "RBLG11.SA", "RDES11.SA", "RDPG11.SA", "RECR11.SA", "RECT11.SA", "RNDP11.SA", "RURA11.SA", "RZAK11.SA", "RZAT11.SA", "RZTR11.SA", "SAAG11.SA", "SANB11.SA", "SARE11.SA", "SBPO11.SA", "SDIL11.SA", "SHPH11.SA", "SMAL11.SA", "SNAG11.SA", "SNCI11.SA", "SPXB11.SA", "SPXI11.SA", "SPVJ11.SA", "SPTW11.SA", "TAEE11.SA", "TECK11.SA", "TGAR11.SA", "TORD11.SA", "TRNT11.SA", "TRXF11.SA", "URPR11.SA", "USTK11.SA", "VCRA11.SA", "VGIA11.SA", "VGIP11.SA", "VGIR11.SA", "VGHT11.SA", "VILG11.SA", "VINO11.SA", "VISC11.SA", "VLOL11.SA", "VSLH11.SA", "VTLT11.SA", "WHGR11.SA", "WTSP11.SA", "XINA11.SA", "XMAL11.SA", "XPIN11.SA", "XPLG11.SA", "XPML11.SA", "XPSF11.SA"
]

def enviar_notificacao_ntfy(titulo, mensagem, prioridade="default", tags=None):
    topico = "Yeild_B3"
    url = f"https://ntfy.sh/{topico}"
    headers = {"Title": titulo, "Priority": prioridade}
    if tags: headers["Tags"] = tags
    
    ntfy_token = os.getenv("NTFY_TOKEN")
    if ntfy_token: headers["Authorization"] = f"Bearer {ntfy_token}"
    
    try:
        response = requests.post(url, data=mensagem.encode('utf-8'), headers=headers, timeout=10)
        response.raise_for_status()
        print("Notificação enviada com sucesso para o ntfy!")
    except Exception as e:
        print(f"Erro ao enviar notificação para o ntfy: {e}")

def buscar_proventos_geral():
    token_brapi = os.getenv("BRAPI_TOKEN", "")
    
    hoje = pd.Timestamp.now().normalize()
    inicio_janela = hoje - pd.Timedelta(days=60)
    fim_janela = hoje + pd.Timedelta(days=60)
    
    proventos_encontrados = []
    
    # Monta parte do token para URL se ele existir
    param_token = f"&token={token_brapi}" if token_brapi else ""
    headers = {"Authorization": f"Bearer {token_brapi}"} if token_brapi else {}

    # 1. Consulta Ações (v2/stocks/dividends)
    if TICKERS_ACOES:
        tickers_acoes_limpos = [t.replace(".SA", "") for t in TICKERS_ACOES]
        lotes_acoes = [tickers_acoes_limpos[i : i + 10] for i in range(0, len(tickers_acoes_limpos), 10)]
        
        print(f"Varrendo ações em {len(lotes_acoes)} lotes...")
        for lote in lotes_acoes:
            symbols = ",".join(lote)
            url = f"https://brapi.dev/api/v2/stocks/dividends?symbols={symbols}{param_token}"
            try:
                res = requests.get(url, headers=headers, timeout=15)
                if res.status_code == 200:
                    dados = res.json()
                    for stock in dados.get("stocks", []):
                        ticker = stock.get("symbol")
                        for item in stock.get("cashDividends", []):
                            data_com_str = item.get("lastDatePrior") or item.get("cutOffDate") or item.get("approvedOn")
                            if not data_com_str: continue
                            
                            try:
                                data_com = pd.to_datetime(data_com_str).tz_localize(None).normalize()
                                if inicio_janela <= data_com <= fim_janela:
                                    tipo = item.get("label", "Dividendo/JCP")
                                    valor = item.get("rate", 0)
                                    proventos_encontrados.append(
                                        f"{ticker}: {tipo} | Data COM: {data_com.strftime('%d/%m')} | R$ {valor}"
                                    )
                            except Exception:
                                continue
            except Exception as e:
                print(f"Erro no lote de ações: {e}")

    # 2. Consulta FIIs (v2/fii/dividends)
    if TICKERS_FIIS:
        tickers_fiis_limpos = [t.replace(".SA", "") for t in TICKERS_FIIS]
        print("Varrendo FIIs...")
        for ticker in tickers_fiis_limpos:
            url = f"https://brapi.dev/api/v2/fii/dividends?symbols={ticker}{param_token}"
            try:
                res = requests.get(url, headers=headers, timeout=15)
                if res.status_code == 200:
                    dados = res.json()
                    for item in dados.get("dividends", []):
                        data_com_str = item.get("lastDatePrior") or item.get("dataCom") or item.get("approvedOn")
                        if not data_com_str: continue
                        
                        try:
                            data_com = pd.to_datetime(data_com_str).tz_localize(None).normalize()
                            if inicio_janela <= data_com <= fim_janela:
                                valor = item.get("rate", 0) or item.get("cashDividends", 0) or item.get("value", 0)
                                proventos_encontrados.append(
                                    f"{ticker} (FII): Rendimento | Data COM: {data_com.strftime('%d/%m')} | R$ {valor}"
                                )
                        except Exception:
                            continue
            except Exception as e:
                print(f"Erro no FII {ticker}: {e}")
                
    return list(set(proventos_encontrados))

if __name__ == "__main__":
    resultados = buscar_proventos_geral()
    
    print(f"Total de proventos encontrados: {len(resultados)}")
    
    if resultados:
        msg = "\n".join(resultados)
        print(f"\nProventos:\n{msg}")
        enviar_notificacao_ntfy("Proventos Detectados", msg, tags="moneybag")
    else:
        print("Nenhum provento encontrado no período.")
        
