import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

# -------- CONFIGURAÇÃO --------
st.set_page_config(page_title="Robô IA do Brasileirão", layout="wide")

API_KEY = "92a41702d74e41fc85bd77effd476f44"
headers = {'X-Auth-Token': API_KEY}
url = "https://api.football-data.org/v4/competitions/BSA/matches"

# -------- MENU LATERAL --------
menu = st.sidebar.selectbox(
    "📂 Selecione uma seção:",
    ("🏟 Jogos do Dia", "🎯 Análise de Valor", "💰 Gestão de Banca (em breve)")
)

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

            # Tabela de jogos
            lista_simples.append({
                "Data": data_jogo,
                "Hora": hora_jogo,
                "Time A": time_a,
                "Time B": time_b,
                "Status": status
            })

            # Simulação de odd + EV
            odd_over25 = round(random.uniform(1.70, 2.30), 2)
            prob_estimada = 0.60
            ev = (prob_estimada * odd_over25) - 1
            valor_aposta = "✅ Valor" if ev > 0 else "❌ Sem valor"

            lista_valor.append({
                "Time A": time_a,
                "Time B": time_b,
                "Odd Over 2.5": f"{odd_over25:.2f}",
                "EV (60%)": f"{ev:.2f}",
                "Tem valor?": valor_aposta
            })

    # -------- CONTEÚDO DINÂMICO --------
    if menu == "🏟 Jogos do Dia":
        st.title("📅 Jogos do Dia (Brasileirão)")
        df_simples = pd.DataFrame(lista_simples)
        if df_simples.empty:
            st.info("⚠️ Não há jogos hoje.")
        else:
            st.dataframe(df_simples, use_container_width=True)

    elif menu == "🎯 Análise de Valor":
        st.title("🎯 Análise de Odds Over 2.5 e Valor Esperado")
        df_valor = pd.DataFrame(lista_valor)
        if df_valor.empty:
            st.info("⚠️ Sem dados de valor esperado.")
        else:
            st.dataframe(df_valor, use_container_width=True)

    elif menu == "💰 Gestão de Banca (em breve)":
        st.title("💰 Gestão de Banca")
        st.warning("Essa funcionalidade está em desenvolvimento. Em breve você poderá acompanhar sua banca, ROI, acertos e perdas.")
else:
    st.error("Erro ao buscar dados da API.")
