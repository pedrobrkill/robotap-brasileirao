import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import requests

# Configuração da página
st.set_page_config(
    page_title="Robo Tap Brasil - Análise de Apostas",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
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

class BrasileiraoAPI:
    def __init__(self, api_key=None):
        self.base_url = "https://api.football-data.org/v4"
        self.headers = {
            "X-Auth-Token": api_key if api_key else "YOUR_API_KEY_HERE"
        }
        self.brasileirao_id = 2013
    
    def get_matches_by_date_range(self, date_from, date_to):
        url = f"{self.base_url}/competitions/{self.brasileirao_id}/matches"
        params = {
            "dateFrom": date_from,
            "dateTo": date_to
        }
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na API: {e}")
            return None
    
    def get_today_matches(self):
        today = datetime.now().date().strftime("%Y-%m-%d")
        data = self.get_matches_by_date_range(today, today)
        
        if data and 'matches' in data:
            return self._process_matches_data(data['matches'], "hoje")
        return pd.DataFrame()
    
    def get_tomorrow_matches(self):
        tomorrow = (datetime.now().date() + timedelta(days=1)).strftime("%Y-%m-%d")
        data = self.get_matches_by_date_range(tomorrow, tomorrow)
        
        if data and 'matches' in data:
            return self._process_matches_data(data['matches'], "amanha")
        return pd.DataFrame()
    
    def get_past_matches(self, days_back=7):
        date_to = datetime.now().date()
        date_from = date_to - timedelta(days=days_back)
        
        data = self.get_matches_by_date_range(
            date_from.strftime("%Y-%m-%d"),
            date_to.strftime("%Y-%m-%d")
        )
        
        if data and 'matches' in data:
            return self._process_matches_data(data['matches'], "passados")
        return pd.DataFrame()
    
    def get_future_matches(self, days_ahead=30):
        date_from = datetime.now().date() + timedelta(days=1)
        date_to = date_from + timedelta(days=days_ahead)
        
        data = self.get_matches_by_date_range(
            date_from.strftime("%Y-%m-%d"),
            date_to.strftime("%Y-%m-%d")
        )
        
        if data and 'matches' in data:
            return self._process_matches_data(data['matches'], "futuros")
        return pd.DataFrame()
    
    def _process_matches_data(self, matches, tipo_jogo):
        processed_matches = []
        
        for match in matches:
            match_date = datetime.fromisoformat(match['utcDate'].replace('Z', '+00:00'))
            match_date_br = match_date - timedelta(hours=3)
            
            processed_match = {
                'id': match['id'],
                'data': match_date_br.strftime('%Y-%m-%d'),
                'hora': match_date_br.strftime('%H:%M'),
                'data_completa': match_date_br,
                'rodada': match.get('matchday', 'N/A'),
                'status': match['status'],
                'casa': match['homeTeam']['name'],
                'casa_id': match['homeTeam']['id'],
                'visitante': match['awayTeam']['name'],
                'visitante_id': match['awayTeam']['id'],
                'tipo_jogo': tipo_jogo
            }
            
            if match['status'] == 'FINISHED':
                processed_match.update({
                    'gols_casa': match['score']['fullTime']['home'],
                    'gols_visitante': match['score']['fullTime']['away'],
                    'resultado': self._get_match_result(
                        match['score']['fullTime']['home'],
                        match['score']['fullTime']['away']
                    )
                })
            else:
                processed_match.update({
                    'gols_casa': None,
                    'gols_visitante': None,
                    'resultado': None
                })
            
            processed_matches.append(processed_match)
        
        return pd.DataFrame(processed_matches)
    
    def _get_match_result(self, home_goals, away_goals):
        if home_goals > away_goals:
            return "Casa"
        elif away_goals > home_goals:
            return "Visitante"
        else:
            return "Empate"
    
    def get_standings(self):
        url = f"{self.base_url}/competitions/{self.brasileirao_id}/standings"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            
            standings = []
            for team in data['standings'][0]['table']:
                standings.append({
                    'posicao': team['position'],
                    'time': team['team']['name'],
                    'jogos': team['playedGames'],
                    'vitorias': team['won'],
                    'empates': team['draw'],
                    'derrotas': team['lost'],
                    'gols_pro': team['goalsFor'],
                    'gols_contra': team['goalsAgainst'],
                    'saldo_gols': team['goalDifference'],
                    'pontos': team['points']
                })
            
            return pd.DataFrame(standings)
            
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao buscar classificação: {e}")
            return pd.DataFrame()

# Função para simular previsões da IA
def add_ai_predictions(df):
    if df.empty:
        return df
    
    df = df.copy()
    predictions = ["Casa", "Empate", "Visitante"]
    
    for idx in df.index:
        df.loc[idx, 'previsao_ia'] = np.random.choice(predictions)
        df.loc[idx, 'confianca'] = np.random.randint(60, 95)
    
    return df

# Inicializar a API
@st.cache_resource
def init_api():
    return BrasileiraoAPI()

# Título principal
st.markdown("""
<div class="main-header">
    <h1>🤖 Robo Tap Brasil - Análise Inteligente de Apostas</h1>
    <p>Dados reais do Brasileirão com previsões baseadas em IA</p>
</div>
""", unsafe_allow_html=True)

# Inicializar API
api = init_api()

# Sidebar
st.sidebar.header("⚙️ Configurações")
refresh_data = st.sidebar.button("🔄 Atualizar Dados")
show_predictions = st.sidebar.checkbox("Mostrar Previsões IA", value=True)

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Jogos Hoje", "📅 Jogos Amanhã", "📊 Jogos Passados", "🔮 Jogos Futuros"])

with tab1:
    st.header("🏆 Jogos de Hoje")
    
    with st.spinner("Buscando jogos de hoje..."):
        jogos_hoje = api.get_today_matches()
        
        if not jogos_hoje.empty:
            if show_predictions:
                jogos_hoje = add_ai_predictions(jogos_hoje)
            
            for _, jogo in jogos_hoje.iterrows():
                col1, col2, col3 = st.columns([3, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="game-card">
                        <h4>{jogo['casa']} vs {jogo['visitante']}</h4>
                        <p><strong>Horário:</strong> {jogo['hora']}</p>
                        <p><strong>Rodada:</strong> {jogo['rodada']}</p>
                        <p><strong>Status:</strong> {jogo['status']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if jogo['gols_casa'] is not None:
                        st.metric("Placar Final", f"{jogo['gols_casa']} x {jogo['gols_visitante']}")
                        st.success(f"Resultado: {jogo['resultado']}")
                    else:
                        st.info("Jogo não iniciado")
                
                with col3:
                    if show_predictions and 'previsao_ia' in jogo:
                        # Corrigido: linha que estava causando erro
                        if jogo['confianca'] >= 80:
                            confidence_class = "prediction-high"
                        elif jogo['confianca'] >= 70:
                            confidence_class = "prediction-medium"
                        else:
                            confidence_class = "prediction-low"
                        
                        st.markdown(f"""
                        <div class="{confidence_class}">
                            <strong>Previsão IA:</strong> {jogo['previsao_ia']}<br>
                            <strong>Confiança:</strong> {jogo['confianca']}%
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("Nenhum jogo hoje no Brasileirão")

with tab2:
    st.header("📅 Jogos de Amanhã")
    
    with st.spinner("Buscando jogos de amanhã..."):
        jogos_amanha = api.get_tomorrow_matches()
        
        if not jogos_amanha.empty:
            if show_predictions:
                jogos_amanha = add_ai_predictions(jogos_amanha)
            
            for _, jogo in jogos_amanha.iterrows():
                col1, col2, col3 = st.columns([3, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="game-card">
                        <h4>{jogo['casa']} vs {jogo['visitante']}</h4>
                        <p><strong>Horário:</strong> {jogo['hora']}</p>
                        <p><strong>Rodada:</strong> {jogo['rodada']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.info("Aguardando jogo")
                
                with col3:
                    if show_predictions and 'previsao_ia' in jogo:
                        # Corrigido: linha que estava causando erro
                        if jogo['confianca'] >= 80:
                            confidence_class = "prediction-high"
                        elif jogo['confianca'] >= 70:
                            confidence_class = "prediction-medium"
                        else:
                            confidence_class = "prediction-low"
                        
                        st.markdown(f"""
                        <div class="{confidence_class}">
                            <strong>Previsão IA:</strong> {jogo['previsao_ia']}<br>
                            <strong>Confiança:</strong> {jogo['confianca']}%
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("Nenhum jogo amanhã no Brasileirão")

with tab3:
    st.header("📊 Jogos Passados")
    
    days_back = st.slider("Dias para buscar", 1, 30, 7)
    
    with st.spinner("Buscando jogos passados..."):
        jogos_passados = api.get_past_matches(days_back)
        
        if not jogos_passados.empty:
            # Filtrar apenas jogos finalizados
            jogos_finalizados = jogos_passados[jogos_passados['status'] == 'FINISHED']
            
            if not jogos_finalizados.empty:
                st.subheader("Resultados dos Jogos")
                
                for _, jogo in jogos_finalizados.iterrows():
                    col1, col2, col3 = st.columns([3, 2, 2])
                    
                    with col1:
                        st.markdown(f"""
                        <div class="game-card">
                            <h4>{jogo['casa']} vs {jogo['visitante']}</h4>
                            <p><strong>Data:</strong> {jogo['data']}</p>
                            <p><strong>Rodada:</strong> {jogo['rodada']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        st.metric("Placar Final", f"{jogo['gols_casa']} x {jogo['gols_visitante']}")
                        
                        if jogo['resultado'] == "Casa":
                            st.success(f"Vitória: {jogo['casa']}")
                        elif jogo['resultado'] == "Visitante":
                            st.success(f"Vitória: {jogo['visitante']}")
                        else:
                            st.info("Empate")
                    
                    with col3:
                        # Mostrar estatísticas do jogo
                        st.write("**Estatísticas:**")
                        st.write(f"Gols: {jogo['gols_casa'] + jogo['gols_visitante']}")
                    
                    st.markdown("---")
                
                # Gráfico de resultados
                if len(jogos_finalizados) > 0:
                    st.subheader("Distribuição de Resultados")
                    result_counts = jogos_finalizados['resultado'].value_counts()
                    fig = px.pie(values=result_counts.values, names=result_counts.index, 
                                title="Distribuição de Resultados nos Últimos Jogos")
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Nenhum jogo finalizado no período selecionado")
        else:
            st.info("Nenhum jogo encontrado no período selecionado")

with tab4:
    st.header("🔮 Próximos Jogos")
    
    days_ahead = st.slider("Dias para buscar", 1, 60, 30)
    
    with st.spinner("Buscando próximos jogos..."):
        jogos_futuros = api.get_future_matches(days_ahead)
        
        if not jogos_futuros.empty:
            if show_predictions:
                jogos_futuros = add_ai_predictions(jogos_futuros)
            
            st.subheader("Calendário de Jogos")
            
            for _, jogo in jogos_futuros.iterrows():
                col1, col2, col3 = st.columns([3, 2, 2])
                
                with col1:
                    st.markdown(f"""
                    <div class="game-card">
                        <h4>{jogo['casa']} vs {jogo['visitante']}</h4>
                        <p><strong>Data:</strong> {jogo['data']}</p>
                        <p><strong>Horário:</strong> {jogo['hora']}</p>
                        <p><strong>Rodada:</strong> {jogo['rodada']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.info("Aguardando jogo")
                
                with col3:
                    if show_predictions and 'previsao_ia' in jogo:
                        # Corrigido: linha que estava causando erro
                        if jogo['confianca'] >= 80:
                            confidence_class = "prediction-high"
                        elif jogo['confianca'] >= 70:
                            confidence_class = "prediction-medium"
                        else:
                            confidence_class = "prediction-low"
                        
                        st.markdown(f"""
                        <div class="{confidence_class}">
                            <strong>Previsão IA:</strong> {jogo['previsao_ia']}<br>
                            <strong>Confiança:</strong> {jogo['confianca']}%
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("Nenhum jogo futuro encontrado no período selecionado")

# Adicionar classificação na sidebar
st.sidebar.markdown("---")
st.sidebar.header("📊 Classificação Atual")

try:
    with st.spinner("Carregando classificação..."):
        classificacao = api.get_standings()
        
        if not classificacao.empty:
            # Mostrar top 6 na sidebar
            top_6 = classificacao.head(6)
            
            for _, time in top_6.iterrows():
                st.sidebar.write(f"{time['posicao']}º {time['time']} - {time['pontos']} pts")
        else:
            st.sidebar.write("Classificação indisponível")
except:
    st.sidebar.write("Erro ao carregar classificação")

# Footer
st.markdown("---")
st.markdown("**🔄 Dados atualizados em tempo real** | **🤖 Powered by IA**")
st.markdown("*Desenvolvido por Robo Tap Brasil*")
