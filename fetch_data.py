import requests
import pandas as pd
import streamlit as st

API_BASE = "https://api.bitget.com"
SYMBOL   = "BTCUSDT"
PERIODS  = {"1H": "1hour", "4H": "4hour", "1D": "1day"}

def fetch_and_process_candles(timeframe: str) -> pd.DataFrame:
    """
    Busca candles de futuros USDT-margined na Bitget e retorna um DataFrame.
    """
    period = PERIODS.get(timeframe, timeframe)
    url    = f"{API_BASE}/api/mix/v1/market/candles"
    params = {"symbol": SYMBOL, "period": period, "limit": 100}
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

    data = payload.get("data", [])
    # Cada item: [timestamp, open, high, low, close, volume]
    if not data:
        st.warning("Nenhum dado de candle retornado para este timeframe.")
        return pd.DataFrame()

    df = pd.DataFrame(data, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df[["open","high","low","close","volume"]] = df[["open","high","low","close","volume"]].astype(float)
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
