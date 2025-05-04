import requests
import pandas as pd
import streamlit as st

# Base da API de futuros USDT-margined (Mix V2)
API_BASE = "https://api.bitget.com"
SYMBOL   = "BTCUSDT"
PRODUCT  = "usdt-futures"        # tudo em minúsculas
PERIODS  = {"1H": "1h", "4H": "4h", "1D": "1d"}  # granularity em minúsculas

def fetch_and_process_candles(timeframe: str) -> pd.DataFrame:
    """
    Busca candles de futuros USDT-margined na Bitget (Mix V2) e retorna um DataFrame.
    """
    gran = PERIODS.get(timeframe, timeframe).lower()
    url  = f"{API_BASE}/api/v2/mix/market/candles"
    params = {
        "symbol":      SYMBOL,
        "granularity": gran,
        "limit":       100,
        "productType": PRODUCT
    }

    try:
        resp = requests.get(url, params=params, timeout=10)
    except requests.RequestException as e:
        st.error(f"Erro de rede ao buscar candles: {e}")
        return pd.DataFrame()

    if resp.status_code != 200:
        st.error(f"Erro {resp.status_code} da API Bitget: {resp.text}")
        return pd.DataFrame()

    try:
        payload = resp.json()
    except ValueError:
        st.error(f"Resposta inválida da API: {resp.text}")
        return pd.DataFrame()

    # Se a API retornar um código próprio no corpo, trate também:
    if payload.get("code") and payload["code"] != "00000":
        st.error(f"Erro {payload['code']} da Bitget: {payload.get('msg')}")
        return pd.DataFrame()

    data = payload.get("data") or []
    if not data:
        st.warning("Nenhum dado de candle retornado para este timeframe.")
        return pd.DataFrame()

    # Monta o DataFrame
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df[["open","high","low","close","volume"]] = \
        df[["open","high","low","close","volume"]].astype(float)
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df


