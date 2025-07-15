import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -------- CONFIGURAÇÃO --------
API_KEY = "92a41702d74e41fc85bd77effd476f44"
headers = {'X-Auth-Token': API_KEY}
url = "https://api.football-data.org/v4/competitions/BSA/matches"

# -------- REQUISIÇÃO --------
response = requests.get(url, headers=headers)

if response.status_code == 200:
    dados = response.json()
    partidas = dados['matches']

    lista_jogos = []
    hoje = datetime.utcnow().strftime('%Y-%m-%d')

    for jogo in partidas:
        data_jogo = jogo["utcDate"][:10]
        if jogo["status"] in ["SCHEDULED", "LIVE"] and data_jogo == hoje:
            time_a = jogo["homeTeam"]["name"]
            time_b = jogo["awayTeam"]["name"]

            # Simula odd para Over 2.5 (você pode substituir depois por uma real via API externa)
            import random
            odd_over25 = round(random.uniform(1.70, 2.30), 2)  # Simulação
            prob_estimada = 0.60  # Estimativa fixa por enquanto

            ev = (prob_estimada * odd_over25) - 1
            valor_aposta = "✅ Valor" if ev > 0 else "❌ Sem valor"

            lista_jogos.append({
                "Time A": time_a,
                "Time B": time_b,
                "Odd Over 2.5": f"{odd_over25:.2f}",
                "EV (60%)": f"{ev:.2f}",
                "Tem valor?": valor_aposta
            })

    df = pd.DataFrame(lista_jogos)

    # -------- INTERFACE STREAMLIT --------
    st.set_page_config(page_title="Robô de Odds", layout="wide")
    st.title("🎯 Jogos do Brasileirão com Odds Over 2.5 e Valor Esperado")

    if df.empty:
        st.warning("⚠️ Não há jogos com dados disponíveis hoje.")
    else:
        st.dataframe(df, use_container_width=True)

else:
    st.error("Erro ao buscar dados da API.")

