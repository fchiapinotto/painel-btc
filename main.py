import streamlit as st
from datetime import datetime

from styles import set_custom_styles
from fetch_data import fetch_and_process_candles
from indicators import compute_all_indicators, extract_supports_resistances
from extract_info import extract_high_level_signals
from charts import (
    render_top_card,
    render_candles_bollinger,
    render_indicators_table,
    render_alerts_table,
    render_grid_scenarios_cards
)
from gpt_analysis import gpt_highlight, gpt_grid_scenarios

# Página Streamlit
st.set_page_config(layout="wide", page_title="Painel Bitget BTC/USDT")
set_custom_styles()

# Carregamento de dados e indicadores (cache 60s)
@st.cache_data(ttl=60)
def load_data(timeframe: str = "1H"):
    df = fetch_and_process_candles(timeframe)
    if df.empty:
        return df, {}, {}
    ind = compute_all_indicators(df)
    sr = extract_supports_resistances(df)
    signals = extract_high_level_signals(ind)
    return df, ind, sr, signals

# Puxa dados para 1H
df, ind, sr, signals = load_data("1H")
if df.empty:
    st.error("❌ Não foi possível carregar dados. Tente novamente mais tarde.")
    st.stop()

# Top Card
render_top_card(df, signals)

# Layout principal
col_main, col_side = st.columns([2, 1])
with col_main:
    render_candles_bollinger(df, sr)
with col_side:
    # Highlight (cache 1h)
    highlight = gpt_highlight(df, signals)
    st.markdown("### 🤖 Insight Rápido")
    st.write(highlight.get("sentenca", ""))
    for b in highlight.get("bullets", []):
        st.write(f"- {b}")

    # Alertas de Grid Trading
    st.markdown("### 🚨 Alertas de Grid")
    alerts = gpt_grid_scenarios(df, signals)
    render_alerts_table(alerts)

# Indicadores Técnicos
st.markdown("### 📊 Indicadores Técnicos")
render_indicators_table(ind)

# Cenários de Grid Trading
st.markdown("### 📋 Cenários de Grid Trading")
render_grid_scenarios_cards(alerts)
