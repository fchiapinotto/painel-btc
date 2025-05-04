import openai
import streamlit as st
from openai.error import RateLimitError, OpenAIError

# Configure sua chave de API no .streamlit/secrets.toml sob [openai]
openai.api_key = st.secrets["openai"]["openai_api_key"]

@st.cache_data(ttl=7 * 24 * 3600)  # 7 dias
def gpt_events() -> list[str]:
    """Retorna uma lista de eventos relevantes (atualiza apenas 1× por semana)."""
    prompt = "Liste eventos relevantes de criptomoedas para hoje e próximos 7 dias."
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        # Assumimos que cada linha é um evento
        return [line.strip() for line in resp.choices[0].message.content.split("\n") if line.strip()]
    except RateLimitError:
        st.warning("⚠️ Limite de taxa atingido para eventos. Tente novamente em alguns dias.")
        return []
    except OpenAIError as e:
        st.error(f"❌ Erro ao consultar OpenAI (events): {e}")
        return []

@st.cache_data(ttl=3600)  # 1 hora
def gpt_highlight(df, signals) -> dict:
    """Gera um highlight curto da cotação + sinais (1× por hora)."""
    price = df["close"].iloc[-1]
    prompt = (
        f"Faça um highlight da cotação atual de BTC/USDT ({price:.2f}) "
        f"e dos principais sinais: {signals}."
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "]()
