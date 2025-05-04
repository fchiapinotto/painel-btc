import streamlit as st

# MUST be the very first Streamlit command:
st.set_page_config(layout="wide", page_title="Painel Bitget BTC/USDT")

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

# Aplica CSS e tema light
set_custom_styles()

# 1) Carregamento de dados e indicadores (cache de 60s)
@st.cache_data(ttl=60)
def load_data(timeframe: str = "1H"):
    df = fetch_and_process_candles(timeframe)
    if df.empty:
        # Retorna vazios para não quebrar o pipeline
        return df, {}, {}, {}
    ind = compute_all_indicators(df)
    sr = extract_supports_resistances(df)
    signals = extract_high_level_signals(ind)
    return df, ind, sr, signals

# Puxa dados para 1H
df, ind, sr, signals = load_data("1H")

# 2) Verificação de erro
if df.empty:
    st.error("❌ Não foi possível carregar dados de candles. Tente novamente mais tarde.")
    st.stop()

# 3) Top Card com preço, variação e badges
render_top_card(df, signals)

# 4) Layout principal: Gráfico & Sidebar de GPT
col_main, col_side = st.columns([2, 1])

with col_main:
    render_candles_bollinger(df, sr)

with col_side:
    # Eventos (cache diário)
    events = gpt_events()
    # Highlight rápido (cache 15min)
    highlight = gpt_highlight(df, signals)
    st.markdown("### 🤖 Insight Rápido")
    st.write(highlight["sentenca"])
    for b in highlight["bullets"]:
        st.write(f"- {b}")

    # Alertas de Grid Trading
    st.markdown("### 🚨 Alertas de Grid")
    alerts = gpt_grid_scenarios(df, signals, events)
    render_alerts_table(alerts)

# 5) Tabela de Indicadores
st.markdown("### 📊 Indicadores Técnicos")
render_indicators_table(ind)

# 6) Cards de Cenários de Grid Trading
st.markdown("### 📋 Cenários de Grid Trading")
render_grid_scenarios_cards(alerts)

# 7) Lista de Eventos Relevantes
st.markdown("### 🗓️ Eventos Relevantes")
render_events_list(events)
