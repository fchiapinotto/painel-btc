import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_top_card(df, signals):
    last = df['close'].iloc[-1]
    prev = df['close'].iloc[-2]
    var = (last - prev) / prev * 100
    st.metric("BTC/USDT", f"{last:,.2f}", f"{var:.2f}%")
    st.write(f"**Sentimento:** {signals.get('sentimento', '')}")
    st.write(f"**Tendência:** {signals.get('tendencia', '')}")
    st.write(f"**Força:** {signals.get('forca_tendencia', '')}")

def render_candles_bollinger(df, sr=None):
    df24 = df.tail(24)
    fig = go.Figure([
        go.Candlestick(
            x=df24['timestamp'], open=df24['open'], high=df24['high'],
            low=df24['low'], close=df24['close'], name='Candles'
        )
    ])
    # Bollinger Bands simples
    middle = df24['close'].rolling(20).mean()
    fig.add_trace(go.Scatter(x=df24['timestamp'], y=middle, name='BB Média'))
    if sr:
        fig.add_hline(y=sr.get('support'), line_dash="dash", annotation_text="Suporte")
        fig.add_hline(y=sr.get('resistance'), line_dash="dash", annotation_text="Resistência")
    fig.update_layout(xaxis_title='Hora', yaxis_title='Preço (USDT)', height=400)
    st.plotly_chart(fig, use_container_width=True)

def render_indicators_table(ind: dict):
    df = pd.DataFrame([ind], index=['1H'])
    st.table(df.T)

def render_alerts_table(alerts: list):
    if not alerts:
        st.info("Nenhum alerta de grid trading no momento.")
        return
    df = pd.DataFrame(alerts)
    st.table(df)

def render_grid_scenarios_cards(scenarios: list):
    if not scenarios:
        st.info("Nenhum cenário de grid disponível no momento.")
        return
    cols = st.columns(len(scenarios))
    for col, sc in zip(cols, scenarios):
        with col:
            st.markdown(f"### {sc.get('tipo', '')}")
            for k, v in sc.items():
                if k != 'tipo':
                    st.write(f"**{k.capitalize()}:** {v}")

def render_events_list(events: list):
    """Renderiza a lista de eventos, que podem ser strings ou dicts."""
    if not events:
        st.info("Nenhum evento relevante disponível no momento.")
        return
    for e in events:
        if isinstance(e, dict):
            date = e.get('date', '')
            title = e.get('title', '')
            st.write(f"- {date} — {title}")
        else:
            st.write(f"- {e}")
