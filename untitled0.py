import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random
import pytz

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

    utc = pytz.utc
    brasilia = pytz.timezone("America/Sao_Paulo")

    agora = datetime.now(brasilia)
    ano_atual = agora.year
    mes_atual = agora.month
    hoje_date = agora.date()

    if mes_atual == 12:
        proximo_mes = 1
        ano_proximo_mes = ano_atual + 1
    else:
        proximo_mes = mes_atual + 1
        ano_proximo_mes = ano_atual

    lista_dia = []
    lista_futuros = []
    lista_valor = []

    for jogo in partidas:
        utc_str = jogo["utcDate"]
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_dt = utc.localize(utc_dt)
        brasilia_dt = utc_dt.astimezone(brasilia)
        data_jogo_date = brasilia_dt.date()

        hora_jogo = brasilia_dt.strftime('%H:%M')
        time_a = jogo["homeTeam"]["name"]
        time_b = jogo["awayTeam"]["name"]
        status = jogo["status"]

        # Jogos do dia (hoje)
        if status in ["SCHEDULED", "LIVE"] and data_jogo_date == hoje_date:
            lista_dia.append({
                "Data": data_jogo_date.strftime('%Y-%m-%d'),
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

        # Jogos futuros do mês atual E do próximo mês (data >= hoje)
        elif (status == "SCHEDULED" and
              ((brasilia_dt.year == ano_atual and brasilia_dt.month == mes_atual) or
               (brasilia_dt.year == ano_proximo_mes and brasilia_dt.month == proximo_mes)) and
              data_jogo_date >= hoje_date):
            lista_futuros.append({
                "Data": data_jogo_date.strftime('%Y-%m-%d'),
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
        st.title(f"🔮 Próximos Jogos do Brasileirão em {ano_atual}-{mes_atual:02d} e {ano_proximo_mes}-{proximo_mes:02d}")
        df_futuros = pd.DataFrame(lista_futuros)
        if df_futuros.empty:
            st.info("⚠️ Nenhum jogo futuro encontrado para os próximos meses.")
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

st.write(...)
