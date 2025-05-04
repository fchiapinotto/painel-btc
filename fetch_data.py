import requests
import pandas as pd
import streamlit as st

API_BASE = "https://api.bitget.com"
SYMBOL   = "BTCUSDT"
PRODUCT  = "usdt-futures"
# Granularities válidas: 1m,3m,5m,15m,30m,1H,4H,6H,12H,1D,3D,1W,1M,6Hutc,...
PERIODS  = {"1H": "1H", "4H": "4H", "1D": "1D"}

def fetch_and_process_candles(timeframe: str) -> pd.DataFrame:
    """
    Buscar candles de futuros USDT-M na Bitget (V2 Mix) e retornar um DataFrame.
    """
    gran = PERIODS.get(timeframe, timeframe)
    url  = f"{API_BASE}/api/v2/mix/market/candles"
    params = {
        "symbol":      SYMBOL,
        "granularity": gran,
        "limit":       100,
        "productType": PRODUCT
        # você pode adicionar startTime/endTime se precisar de histórico específico
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

    # Alguns endpoints retornam um 'code' interno diferente de 00000 em erro
    if payload.get("code") and payload["code"] != "00000":
        st.error(f"Erro {payload['code']} da Bitget: {payload.get('msg')}")
        return pd.DataFrame()

    data = payload.get("data") or []
    if not data:
        st.warning("Nenhum dado de candle retornado para este timeframe.")
        return pd.DataFrame()

    # Cada item: [timestamp, open, high, low, close, volume]
    df = pd.DataFrame(data, columns=["timestamp","open","high","low","close","volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df[["open","high","low","close","volume"]] = df[["open","high","low","close","volume"]].astype(float)
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

