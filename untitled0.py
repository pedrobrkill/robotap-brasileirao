import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -------- CONFIGURAÇÃO --------
API_KEY = "92a41702d74e41fc85bd77effd476f44"  # SUA API KEY
headers = {'X-Auth-Token': API_KEY}
url = "https://api.football-data.org/v4/competitions/BSA/matches"

# -------- REQUISIÇÃO --------
response = requests.get(url, headers=headers)

# -------- PROCESSAMENTO --------
if response.status_code == 200:
    dados = response.json()
    partidas = dados['matches']

    lista_jogos = []
    for jogo in partidas:
        if jogo["status"] in ["SCHEDULED", "LIVE"]:
            item = {
                "Data": jogo["utcDate"][:10],
                "Hora": jogo["utcDate"][11:16],
                "Time A": jogo["homeTeam"]["name"],
                "Time B": jogo["awayTeam"]["name"],
                "Status": jogo["status"]
            }
            lista_jogos.append(item)

    df = pd.DataFrame(lista_jogos)

    # Filtrar para mostrar apenas os jogos do dia atual
    hoje = datetime.utcnow().strftime('%Y-%m-%d')
    df = df[df["Data"] == hoje]

    # -------- INTERFACE STREAMLIT --------
    st.set_page_config(page_title="Jogos do Brasileirão", layout="wide")
    st.title("📅 Jogos do Brasileirão - Hoje")

    if df.empty:
        st.warning("⚠️ Não há jogos programados para hoje.")
    else:
        st.dataframe(df, use_container_width=True)

else:
    st.error(f"Erro ao buscar dados: {response.status_code}")
