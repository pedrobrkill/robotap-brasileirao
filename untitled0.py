import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random

st.set_page_config(page_title="Robô IA do Brasileirão", layout="wide")

API_KEY = "92a41702d74e41fc85bd77effd476f44"
headers = {'X-Auth-Token': API_KEY}
url = "https://api.football-data.org/v4/competitions/BSA/matches"

menu = st.sidebar.radio("📂 Navegação", [
    "🏟 Jogos do Dia",
    "🔮 Jogos Futuros",
    "🎯 Análise de Valor (Hoje)",
    "💰 Gestão de Banca (em breve)"
])

response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    partidas = dados['matches']
    hoje = datetime.utcnow().strftime('%Y-%m-%d')

    lista_dia = []
    lista_futuros = []
    lista_valor = []

    for jogo in partidas:
        data_jogo = jogo["utcDate"][:10]
        hora_jogo = jogo["utcDate"][11:16]
        time_a = jogo["homeTeam"]["name"]
        time_b = jogo["awayTeam"]["name"]
        status = jogo["status"]

        if status in ["SCHEDULED", "LIVE"] and data_jogo == hoje:
            lista_dia.append({
                "Data": data_jogo,
                "Hora": hora_jogo,
                "Time A": time_a,
                "Time B": time_b,
                "Status": status
            })

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

        elif status == "SCHEDULED" and data_jogo > hoje:
            lista_futuros.append({
                "Data": data_jogo,
                "Hora": hora_jogo,
                "Time A": time_a,
                "Time B": time_b,
                "Status": status
            })

    if menu == "🏟 Jogos do Dia":
        st.title("🏟 Jogos do Dia (Brasileirão)")
        df_dia = pd.DataFrame(lista_dia)
        if df_dia.empty:
            st.info("⚠️ Não há jogos do Brasileirão para hoje.")
        else:
            st.dataframe(df_dia, use_container_width=True)

    elif menu == "🔮 Jogos Futuros":
        st.title("🔮 Próximos Jogos do Brasileirão")
        df_futuros = pd.DataFrame(lista_futuros)
        if df_futuros.empty:
            st.info("⚠️ Nenhum jogo futuro encontrado.")
        else:
            st.dataframe(df_futuros, use_container_width=True)

    elif menu == "🎯 Análise de Valor (Hoje)":
        st.title("🎯 Análise de Valor - Over 2.5 (Somente Hoje)")
        df_valor = pd.DataFrame(lista_valor)
        if df_valor.empty:
            st.info("⚠️ Nenhum jogo hoje para calcular valor.")
        else:
            st.dataframe(df_valor, use_container_width=True)

    elif menu == "💰 Gestão de Banca (em breve)":
        st.title("💰 Gestão de Banca")
        st.warning("Essa funcionalidade estará disponível em breve.")

else:
    st.error("Erro ao buscar dados da API.")
