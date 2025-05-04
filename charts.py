import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_top_card(df, signals):
    last = df['close'].iloc[-1]
    prev = df['close'].iloc[-2]
    var = (last-prev)/prev*100
    st.metric("BTC/USDT", f"{last:,.2f}", f"{var:.2f}%")
    st.write(f"**Sentimento:** {signals['sentimento']}")
    st.write(f"**Tendência:** {signals['tendencia']}")
    st.write(f"**Força:** {signals['forca_tendencia']}")

def render_candles_bollinger(df, sr=None):
    df24 = df.tail(24)
    fig = go.Figure([go.Candlestick(x=df24['timestamp'], open=df24['open'], high=df24['high'], low=df24['low'], close=df24['close'])])
    bb = pd.Series(df24['close']).rolling(20).mean()
    fig.add_trace(go.Scatter(x=df24['timestamp'], y=bb, name='BB Média'))
    if sr:
        fig.add_hline(y=sr['support'], line_dash="dash", annotation_text="Suporte")
        fig.add_hline(y=sr['resistance'], line_dash="dash", annotation_text="Resist.")
    st.plotly_chart(fig, use_container_width=True)

def render_indicators_table(ind: dict):
    df = pd.DataFrame([ind], index=['1H'])
    st.table(df.T)

def render_alerts_table(alerts: list):
    df = pd.DataFrame(alerts)
    st.table(df)

def render_grid_scenarios_cards(scenarios: list):
    cols = st.columns(3)
    for col, sc in zip(cols, scenarios):
        with col:
            st.write(f"### {sc['tipo']}")
            for k,v in sc.items():
                if k!='tipo': st.write(f"**{k}:** {v}")

def render_events_list(events: list):
    for e in events:
        st.write(f"- {e.get('date')} — {e.get('title')}")
