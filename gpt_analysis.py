import openai
import streamlit as st
from openai.error import RateLimitError, OpenAIError

openai.api_key = st.secrets['openai']['openai_api_key']

@st.cache_data(ttl=3600)
def gpt_highlight(df, signals):
    price = df['close'].iloc[-1]
    prompt = (
        f"Highlight da cotação atual ({price:.2f}) e sinais {signals}."
    )
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role':'user','content':prompt}], max_tokens=150
        )
        lines = resp.choices[0].message.content.split("\n")
        return {'sentenca': lines[0], 'bullets': lines[1:]}
    except RateLimitError:
        st.warning("Limite de taxa atingido para highlights. Tente mais tarde.")
        return {'sentenca':'','bullets':[]}
    except OpenAIError as e:
        st.error(f"Erro GPT Highlight: {e}")
        return {'sentenca':'','bullets':[]}

@st.cache_data(ttl=3600)
def gpt_grid_scenarios(df, signals):
    price = df['close'].iloc[-1]
    prompt = (
        f"Proponha 3 cenários de grid trading (Long, Short, Neutro) com preco {price:.2f} e sinais {signals}."
    )
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-4-turbo',
            messages=[{'role':'user','content':prompt}], max_tokens=400
        )
        import json
        return json.loads(resp.choices[0].message.content)
    except (RateLimitError, OpenAIError, Exception) as e:
        st.warning(f"Erro GPT Grid: {e}")
        return []
