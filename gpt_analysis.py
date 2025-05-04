import openai
import streamlit as st

openai.api_key = st.secrets['openai']['openai_api_key']

@st.cache_data(ttl=24*3600)
def gpt_events():
    prompt = "Liste eventos relevantes de criptomoedas para hoje e próximos 7 dias."
    resp = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role':'user','content':prompt}])
    return resp.choices[0].message.content

@st.cache_data(ttl=900)
def gpt_highlight(df, signals):
    prompt = f"Highlight: preço {df['close'].iloc[-1]} e sinais {signals}"
    resp = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role':'user','content':prompt}], max_tokens=150)
    content = resp.choices[0].message.content.split('\n')
    return {'sentenca': content[0], 'bullets': content[1:]}

@st.cache_data(ttl=900)
def gpt_grid_scenarios(df, signals, events):
    prompt = f"Proponha 3 cenários de grid trading (Long, Short, Neutral) com preço {df['close'].iloc[-1]}, sinais {signals}, eventos {events}."
    resp = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{'role':'user','content':prompt}], max_tokens=300)
    return resp.choices[0].message.content

