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
    render_grid_scenarios_cards,
    render_events_list
)
from gpt_analysis import gpt_events, gpt_highlight, gpt_grid_scenarios

set_custom_styles()
st.set_page_config(layout="wide", page_title="Painel Bitget BTC/USDT")

@st.cache_data(ttl=60)
def load_data(timeframe: str = "1H"):
    df = fetch_and_process_candles(timeframe)
    ind = compute_all_indicators(df)
    sr = extract_supports_resistances(df)
    signals = extract_high_level_signals(ind)
    return df, ind, sr, signals

df, ind, sr, signals = load_data("1H")

render_top_card(df, signals)

col_main, col_side = st.columns([2,1])
with col_main:
    render_candles_bollinger(df, sr)
with col_side:
    events = gpt_events()
    highlight = gpt_highlight(df, signals)
    st.markdown("### 🤖 Insight Rápido")
    st.write(highlight["sentenca"])
    for b in highlight["bullets"]:
        st.write(f"- {b}")

    st.markdown("### 🚨 Alertas de Grid")
    alerts = gpt_grid_scenarios(df, signals, events)
    render_alerts_table(alerts)

st.markdown("### 📊 Indicadores Técnicos")
render_indicators_table(ind)

st.markdown("### 📋 Cenários de Grid Trading")
render_grid_scenarios_cards(alerts)

st.markdown("### 🗓️ Eventos Relevantes")
render_events_list(events)
