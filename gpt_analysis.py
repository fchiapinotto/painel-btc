import openai
import streamlit as st
from openai.error import RateLimitError, OpenAIError

openai.api_key = st.secrets['openai']['openai_api_key']

@st.cache_data(ttl=24*3600)
def gpt_events():
    prompt = "Liste eventos relevantes de criptomoedas para hoje e próximos 7 dias."
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role':'user','content':prompt}]
        )
        return resp.choices[0].message.content.split("\n")
    except RateLimitError:
        st.warning("Limite de taxa atingido para eventos. Tente novamente mais tarde.")
        return []
    except OpenAIError as e:
        st.error(f"Erro ao consultar OpenAI: {e}")
        return []

@st.cache_data(ttl=900)
def gpt_highlight(df, signals):
    prompt = (
        f"Highlight da cotação atual {df['close'].iloc[-1]:.2f} e sinais {signals}."  
    )
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role':'user','content':prompt}],
            max_tokens=150
        )
        content = resp.choices[0].message.content.split("\n")
        return {'sentenca': content[0], 'bullets': content[1:]}
    except RateLimitError:
        st.warning("Limite de taxa atingido para highlights. Tente novamente em 15 minutos.")
        return {'sentenca': "", 'bullets': []}
    except OpenAIError as e:
        st.error(f"Erro ao consultar OpenAI: {e}")
        return {'sentenca': "", 'bullets': []}

@st.cache_data(ttl=900)
def gpt_grid_scenarios(df, signals, events=None):
    prompt = (
        f"Proponha 3 cenários de grid trading (Long, Short, Neutro) com preço {df['close'].iloc[-1]:.2f}, sinais {signals}, eventos {events}."
    )
    try:
        resp = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role':'user','content':prompt}],
            max_tokens=300
        )
        # parse JSON-like response here se necessário
        return resp.choices[0].message.content
    except RateLimitError:
        st.warning("Limite de taxa atingido para cenários de grid. Tente novamente em 15 minutos.")
        return []
    except OpenAIError as e:
        st.error(f"Erro ao consultar OpenAI: {e}")
        return []
