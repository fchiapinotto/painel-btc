import openai
import streamlit as st
import json
from openai.error import RateLimitError, OpenAIError

# Configure sua chave de API no .streamlit/secrets.toml sob [openai]
openai.api_key = st.secrets["openai"]["openai_api_key"]

@st.cache_data(ttl=7 * 24 * 3600)
def gpt_events() -> list[str]:
    """Retorna eventos relevantes de criptomoedas para hoje e próximos 7 dias (cache de 7 dias)."""
    prompt = "Liste eventos relevantes de criptomoedas para hoje e próximos 7 dias."
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300
        )
        content = resp.choices[0].message.content
        # Supondo resposta em linhas:
        return [line.strip() for line in content.split("\n") if line.strip()]
    except RateLimitError:
        st.warning("⚠️ Limite de taxa atingido para eventos. Tente novamente depois.")
        return []
    except OpenAIError as e:
        st.error(f"❌ Erro ao consultar OpenAI (events): {e}")
        return []

@st.cache_data(ttl=3600)
def gpt_highlight(df, signals) -> dict:
    """Gera um highlight curto da cotação e sinais (cache de 1 hora)."""
    price = df["close"].iloc[-1]
    prompt = (
        f"Faça um highlight da cotação atual de BTC/USDT ({price:.2f}) "
        f"e dos principais sinais: {signals}."
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )
        lines = resp.choices[0].message.content.split("\n")
        sentence = lines[0].strip()
        bullets = [l.strip() for l in lines[1:] if l.strip()]
        return {"sentenca": sentence, "bullets": bullets}
    except RateLimitError:
        st.warning("⚠️ Limite de taxa atingido para highlights. Tente novamente em 1 hora.")
        return {"sentenca": "", "bullets": []}
    except OpenAIError as e:
        st.error(f"❌ Erro ao consultar OpenAI (highlight): {e}")
        return {"sentenca": "", "bullets": []}

@st.cache_data(ttl=3600)
def gpt_grid_scenarios(df, signals, events=None) -> list[dict]:
    """Proponha 3 cenários de grid trading (Long, Short, Neutro) (cache de 1 hora)."""
    price = df["close"].iloc[-1]
    base = f"Baseado no preço atual de BTC/USDT ({price:.2f}), nos sinais {signals}"
    ev_text = f" e nos eventos {events}" if events else ""
    prompt = (
        base + ev_text +
        ", proponha 3 cenários de grid trading para futuros: Long, Short e Neutro. "
        "Retorne um JSON array de objetos com campos: tipo, momento, risco, faixas, sl_tp, alavancagem, valor_sugerido."
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        content = resp.choices[0].message.content
        # Parse JSON
        scenarios = json.loads(content)
        return scenarios if isinstance(scenarios, list) else []
    except RateLimitError:
        st.warning("⚠️ Limite de taxa atingido para cenários de grid. Tente novamente em 1 hora.")
        return []
    except (OpenAIError, json.JSONDecodeError) as e:
        st.error(f"❌ Erro ao processar cenários de grid: {e}")
        return []
