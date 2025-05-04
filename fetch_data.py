import requests
import pandas as pd
import streamlit as st

API_BASE = "https://api.bitget.com"
SYMBOL   = "BTCUSDT"
PRODUCT  = "usdt-futures"
PERIODS  = {"1H": "1H", "4H": "4H", "1D": "1D"}

def fetch_and_process_candles(timeframe: str) -> pd.DataFrame:
    """
    Busca candles de futuros USDT-M na Bitget (Mix V2) e retorna um DataFrame
    com colunas: timestamp, open, high, low, close, volume.
    """
    gran = PERIODS.get(timeframe, timeframe)
    url  = f"{API_BASE}/api/v2/mix/market/candles"
    params = {
        "symbol":      SYMBOL,
        "granularity": gran,
        "limit":       100,
        "productType": PRODUCT
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        st.error(f"Erro de rede/HTTP ao buscar candles: {e}")
        return pd.DataFrame()

    try:
        payload = resp.json()
    except ValueError:
        st.error(f"Resposta inválida da API: {resp.text}")
        return pd.DataFrame()

    if payload.get("code") and payload["code"] != "00000":
        st.error(f"Erro {payload['code']} da Bitget: {payload.get('msg')}")
        return pd.DataFrame()

    raw = payload.get("data") or []
    if not raw:
        st.warning("Nenhum dado de candle retornado para este timeframe.")
        return pd.DataFrame()

    # 1) lê tudo
    df_raw = pd.DataFrame(raw)
    # 2) detecta número de colunas e renomeia
    if df_raw.shape[1] == 7:
        df_raw.columns = [
            "timestamp", "open", "high", "low", "close", "volume", "quote_volume"
        ]
        df = df_raw.drop(columns=["quote_volume"])
    elif df_raw.shape[1] == 6:
        df_raw.columns = [
            "timestamp", "open", "high", "low", "close", "volume"
        ]
        df = df_raw
    else:
        st.error(f"Dados inesperados: recebi {df_raw.shape[1]} colunas")
        return pd.DataFrame()

    # 3) conversões de tipo e ordenação
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df[["open","high","low","close","volume"]] = df[
        ["open","high","low","close","volume"]
    ].astype(float)
    df.sort_values("timestamp", inplace=True, ignore_index=True)
    return df


