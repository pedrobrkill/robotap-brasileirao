import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# Configuração da página
st.set_page_config(
    page_title="Robo Tap Brasil - Análise de Apostas",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    
    .game-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .prediction-high {
        color: #28a745;
        font-weight: bold;
    }
    
    .prediction-medium {
        color: #ffc107;
        font-weight: bold;
    }
    
    .prediction-low {
        color: #dc3545;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Função para gerar dados fictícios de jogos
@st.cache_data
def generate_sample_games():
    teams = [
        "Flamengo", "Palmeiras", "São Paulo", "Corinthians", "Atlético-MG",
        "Internacional", "Grêmio", "Botafogo", "Vasco", "Fluminense",
        "Santos", "Cruzeiro", "Bahia", "Fortaleza", "Athletico-PR"
    ]
    
    leagues = ["Brasileirão", "Copa do Brasil", "Libertadores", "Sul-Americana"]
    
    games = []
    for i in range(20):
        home_team = random.choice(teams)
        away_team = random.choice([t for t in teams if t != home_team])
        
        # Gerar odds realistas
        home_odds = round(random.uniform(1.5, 4.0), 2)
        draw_odds = round(random.uniform(2.5, 3.8), 2)
        away_odds = round(random.uniform(1.5, 4.0), 2)
        
        # Calcular probabilidades implícitas
        home_prob = round((1/home_odds) * 100, 1)
        draw_prob = round((1/draw_odds) * 100, 1)
        away_prob = round((1/away_odds) * 100, 1)
        
        # Previsão da IA (simulada)
        predictions = ["Casa", "Empate", "Visitante"]
        ai_prediction = random.choice(predictions)
        confidence = round(random.uniform(60, 95), 1)
        
        game = {
            "Data": datetime.now() + timedelta(days=random.randint(0, 7)),
            "Liga": random.choice(leagues),
            "Casa": home_team,
            "Visitante": away_team,
            "Odds Casa": home_odds,
            "Odds Empate": draw_odds,
            "Odds Visitante": away_odds,
            "Prob Casa (%)": home_prob,
            "Prob Empate (%)": draw_prob,
            "Prob Visitante (%)": away_prob,
            "Previsão IA": ai_prediction,
            "Confiança (%)": confidence
        }
        games.append(game)
    
    return pd.DataFrame(games)

# Função para gerar estatísticas da IA
@st.cache_data
def generate_ai_stats():
    return {
        "taxa_acerto": 73.5,
        "jogos_analisados": 1247,
        "lucro_mes": 12.8,
        "melhor_liga": "Brasileirão"
    }

# Título principal
st.markdown("""
<div class="main-header">
    <h1>🤖 Robo Tap Brasil - Análise Inteligente de Apostas</h1>
    <p>Previsões esportivas baseadas em Inteligência Artificial</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("⚙️ Filtros")
selected_league = st.sidebar.selectbox("Liga", ["Todas", "Brasileirão", "Copa do Brasil", "Libertadores", "Sul-Americana"])
selected_date = st.sidebar.date_input("Data", datetime.now().date())
confidence_filter = st.sidebar.slider("Confiança Mínima (%)", 50, 95, 70)

# Carregar dados
games_df = generate_sample_games()
ai_stats = generate_ai_stats()

# Filtrar dados
if selected_league != "Todas":
    games_df = games_df[games_df["Liga"] == selected_league]

games_df = games_df[games_df["Confiança (%)"] >= confidence_filter]

# Métricas principais
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Taxa de Acerto", f"{ai_stats['taxa_acerto']}%", "2.1%")

with col2:
    st.metric("Jogos Analisados", f"{ai_stats['jogos_analisados']:,}", "127")

with col3:
    st.metric("ROI Mensal", f"{ai_stats['lucro_mes']}%", "1.2%")

with col4:
    st.metric("Melhor Liga", ai_stats['melhor_liga'], "")

# Separador
st.markdown("---")

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Jogos do Dia", "📊 Análise Detalhada", "📈 Estatísticas", "🎯 Dicas VIP"])

with tab1:
    st.header("🏆 Jogos do Dia - Previsões da IA")
    
    if len(games_df) > 0:
        # Ordenar por confiança
        games_sorted = games_df.sort_values("Confiança (%)", ascending=False)
        
        for idx, game in games_sorted.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="game-card">
                        <h4>{game['Casa']} vs {game['Visitante']}</h4>
                        <p><strong>Liga:</strong> {game['Liga']}</p>
                        <p><strong>Data:</strong> {game['Data'].strftime('%d/%m/%Y')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Odds:**")
                    st.write(f"Casa: {game['Odds Casa']}")
                    st.write(f"Empate: {game['Odds Empate']}")
                    st.write(f"Visitante: {game['Odds Visitante']}")
                
                with col3:
                    confidence_class = "prediction-high" if game['Confiança (%)'] >= 80 else "prediction-medium" if game['Confiança (%)'] >= 70 else "prediction-low"
                    
                    st.markdown(f"""
                    <div class="{confidence_class}">
                        <strong>Previsão IA:</strong> {game['Previsão IA']}<br>
                        <strong>Confiança:</strong> {game['Confiança (%)']}%
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
    else:
        st.warning("Nenhum jogo encontrado com os filtros aplicados.")

with tab2:
    st.header("📊 Análise Detalhada")
    
    if len(games_df) > 0:
        # Gráfico de distribuição de odds
        fig = px.histogram(games_df, x="Odds Casa", nbins=20, title="Distribuição das Odds para Casa")
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráfico de confiança por liga
        confidence_by_league = games_df.groupby("Liga")["Confiança (%)"].mean().reset_index()
        fig2 = px.bar(confidence_by_league, x="Liga", y="Confiança (%)", title="Confiança Média por Liga")
        st.plotly_chart(fig2, use_container_width=True)
        
        # Tabela detalhada
        st.subheader("Tabela Completa")
        st.dataframe(games_df.style.format({
            "Odds Casa": "{:.2f}",
            "Odds Empate": "{:.2f}",
            "Odds Visitante": "{:.2f}",
            "Prob Casa (%)": "{:.1f}%",
            "Prob Empate (%)": "{:.1f}%",
            "Prob Visitante (%)": "{:.1f}%",
            "Confiança (%)": "{:.1f}%"
        }))

with tab3:
    st.header("📈 Estatísticas da IA")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Performance Geral")
        
        # Gráfico de pizza - distribuição de previsões
        prediction_counts = games_df["Previsão IA"].value_counts()
        fig = px.pie(values=prediction_counts.values, names=prediction_counts.index, 
                    title="Distribuição das Previsões")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Confiança por Tipo de Previsão")
        
        confidence_by_prediction = games_df.groupby("Previsão IA")["Confiança (%)"].mean().reset_index()
        fig = px.bar(confidence_by_prediction, x="Previsão IA", y="Confiança (%)", 
                    title="Confiança Média por Tipo de Previsão")
        st.plotly_chart(fig, use_container_width=True)
    
    # Métricas adicionais
    st.subheader("Métricas Avançadas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_confidence = games_df["Confiança (%)"].mean()
        st.metric("Confiança Média", f"{avg_confidence:.1f}%")
    
    with col2:
        high_confidence_games = len(games_df[games_df["Confiança (%)"] >= 80])
        st.metric("Jogos Alta Confiança", high_confidence_games)
    
    with col3:
        avg_odds = games_df["Odds Casa"].mean()
        st.metric("Odds Média Casa", f"{avg_odds:.2f}")

with tab4:
    st.header("🎯 Dicas VIP")
    
    st.warning("⚠️ Esta seção está disponível apenas para assinantes VIP")
    
    st.markdown("""
    ### Benefícios da Assinatura VIP:
    - 🎯 Dicas exclusivas com maior taxa de acerto
    - 📱 Alertas em tempo real
    - 📊 Análises mais detalhadas
    - 🔔 Notificações de oportunidades
    - 💰 Estratégias de bankroll
    """)
    
    if st.button("Assinar VIP - R$ 29,90/mês"):
        st.success("Redirecionando para o pagamento...")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p>⚠️ <strong>Aviso:</strong> Apostas esportivas envolvem riscos. Aposte com responsabilidade.</p>
    <p>📧 Contato: suporte@robotapbrasil.com | 📞 (11) 9999-9999</p>
</div>
""", unsafe_allow_html=True)
