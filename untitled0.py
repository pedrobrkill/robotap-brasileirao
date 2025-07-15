import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import random
import pytz

# Configuração da página
st.set_page_config(page_title="Robô IA do Brasileirão", layout="wide")

API_KEY = "92a41702d74e41fc85bd77effd476f44"
headers = {'X-Auth-Token': API_KEY}
url = "https://api.football-data.org/v4/competitions/BSA/matches"

# Menu lateral
menu = st.sidebar.radio("📂 Navegação", [
    "🏟 Jogos do Dia",
    "🔮 Jogos Futuros",
    "🎯 Análise de Valor (Hoje)",
    "💰 Gestão de Banca (em breve)"
])

# Faz a requisição
response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    partidas = dados['matches']

    # Fuso horários
    utc = pytz.utc
    brasilia = pytz.timezone("America/Sao_Paulo")

    hoje = datetime.now(brasilia).strftime('%Y-%m-%d')

    lista_dia = []
    lista_futuros = []
    lista_valor = []

    for jogo in partidas:
        utc_str = jogo["utcDate"]
        # Transforma string em datetime UTC
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%SZ")
        utc_dt = utc.localize(utc_dt)
        # Converte para horário de Brasília
        brasilia_dt = utc_dt.astimezone(brasilia)

        data_jogo = brasilia_dt.strftime('%Y-%m-%d')
        hora_jogo = brasilia_dt.strftime('%H:%M')

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
