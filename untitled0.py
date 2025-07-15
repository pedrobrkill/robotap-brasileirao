import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# -------- CONFIG --------
st.set_page_config(page_title="Robô IA do Brasileirão", layout="wide")

API_KEY = "92a41702d74e41fc85bd77effd476f44"
headers = {'X-Auth-Token': API_KEY}
url = "https://api.football-data.org/v4/competitions/BSA/matches"

# -------- MENU LATERAL FIXO --------
menu = st.sidebar.radio("📂 Navegação", ["🏟 Jogos do Dia", "🎯 Análise de Valor", "💰 Gestão de Banca"])

st.sidebar.markdown("---")
st.sidebar.markdown("👨‍💻 Criado com IA")
st.sidebar.markdown("🔗 [robotip-brasileirao.streamlit.app](https://robotap-brasileirao.streamlit.app)")

# -------- REQUISIÇÃO --------
response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    partidas = dados['matches']
    hoje = datetime.utcnow().strftime('%Y-%m-%d')

    lista_simples = []
    lista_valor = []

    for jogo in partidas:
        data_jogo = jogo["utcDate"][:10]
        hora_jogo = jogo["utcDate"][11:16]
        if jogo["status"] in ["SCHEDULED", "LIVE"] and data_jogo == hoje:
            time_a = jogo["homeTeam"]["name"]
            time_b = jogo["awayTeam"]["name"]
            status = jogo["status"]

            lista_simples.append({
                "Data": data_jogo,
                "Hora": hora_jogo,
                "Time
