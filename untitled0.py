import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import random

# Configuração do layout do Streamlit
st.set_page_config(page_title="Robotip Esportiva", layout="wide")
st.title("⚽ Robotip Esportiva - Jogos do Brasileirão")

# Menu lateral
menu = st.sidebar.radio("📂 Menu", [
    "🏟 Jogos do Dia",
    "🔮 Jogos Futuros",
    "🎯 Análise de Valor (Simulada)",
    "💰 Gestão de Banca (em breve)"
])

# URL do Globo Esporte
URL = "https://ge.globo.com/futebol/brasileirao-serie-a/agenda-de-jogos/"

# Função para pegar os jogos do site
def pegar_jogos():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    dias = soup.find_all("div", class_="feed-post-body")
    jogos = []

    for dia in dias:
        try:
            data_txt = dia.find("span", class_="feed-post-datetime")
            if not data_txt:
                continue
            data_txt = data_txt.text.strip()
            data_obj = datetime.strptime(data_txt, "%d/%m").replace(year=datetime.now().year)

            partidas = dia.find_all("li", class_="lista-de-jogos__item")
            for p in partidas:
                times = p.find_all("span", class_="equipes__nome")
                hora = p.find("span", class_="lista-de-jogos__hora")
                if times and len(times) == 2 and hora:
                    jogos.append({
                        "Data": data_obj.strftime("%Y-%m-%d"),
                        "Hora": hora.text.strip(),
                        "Time A": times[0].text.strip(),
                        "Time B": times[1].text.strip()
                    })
        except Exception as e:
            continue

    return pd.DataFrame(jogos)

# Carregar os dados
df = pegar_jogos()
hoje = datetime.now().strftime("%Y-%m-%d")

# Separar jogos do dia e futuros
df_hoje = df[df["Data"] == hoje]
df_futuros = df[df["Data"] > hoje]

# Simular análise de valor
df_valor = df_hoje.copy()
if not df_valor.empty:
    df_valor["Odd Over 2.5"] = df_valor.apply(lambda x: round(random.uniform(1.7, 2.3), 2), axis=1)
    df_valor["EV (60%)"] = df_valor["Odd Over 2.5"].apply(lambda x: round((0.6 * x) - 1, 2))
    df_valor["Tem valor?"] = df_valor["EV (60%)"].apply(lambda x: "✅ Valor" if x > 0 else "❌ Sem valor")

# Exibição conforme o menu
if menu == "🏟 Jogos do Dia":
    st.subheader("🏟 Jogos do Dia")
    if df_hoje.empty:
        st.info("Não há jogos hoje.")
    else:
        st.dataframe(df_hoje, use_container_width=True)

elif menu == "🔮 Jogos Futuros":
    st.subheader("🔮 Jogos Futuros")
    if df_futuros.empty:
        st.info("Nenhum jogo futuro encontrado.")
    else:
        st.dataframe(df_futuros, use_container_width=True)

elif menu == "🎯 Análise de Valor (Simulada)":
    st.subheader("🎯 Análise de Valor - Over 2.5")
    if df_valor.empty:
        st.info("Sem jogos hoje para análise.")
    else:
        st.dataframe(df_valor, use_container_width=True)

elif menu == "💰 Gestão de Banca (em breve)":
    st.subheader("💰 Gestão de Banca")
    st.warning("Essa funcionalidade estará disponível em breve.")
