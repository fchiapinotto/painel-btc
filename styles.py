import streamlit as st

def set_custom_styles():
    st.markdown("""
    <style>
    body { background-color: #ffffff; color: #333333; }
    .stMetric > div { font-size: 2em; }
    .titulo-secao { font-weight: bold; margin-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)
