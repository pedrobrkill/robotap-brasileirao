import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
# Usamos o layout "wide" para aproveitar melhor o espaço e definimos um título para a aba do navegador.
st.set_page_config(layout="wide", page_title="Jogos do Dia")

# --- DADOS DOS JOGOS ---
# Em uma aplicação real, estes dados viriam de uma API ou de um web scraping.
# Para este exemplo, vamos usar os mesmos dados fixos do exemplo anterior.
# Você pode facilmente substituir esta lista por dados dinâmicos.
matches_data = [
    {
        "league": "Brasileirão Série A",
        "countryFlag": "🇧🇷",
        "time": "19:00",
        "homeTeam": {
            "name": "Flamengo",
            "logo": "https://s3.ap-southeast-1.amazonaws.com/images.deccanchronicle.com/dc-Cover-lcf2ab3e8b0a5a709565a5855234551e1-20220521152729.jpeg"
        },
        "awayTeam": {
            "name": "Palmeiras",
            "logo": "https://logodownload.org/wp-content/uploads/2015/05/palmeiras-logo-4.png"
        },
        "predictions": {
            "home": "45%",
            "draw": "30%",
            "away": "25%"
        },
        "bothScore": "60%",
        "over2_5": "55%"
    },
    {
        "league": "Premier League",
        "countryFlag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
        "time": "16:00",
        "homeTeam": {
            "name": "Man. United",
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/7/7a/Manchester_United_FC_crest.svg/1200px-Manchester_United_FC_crest.svg.png"
        },
        "awayTeam": {
            "name": "Liverpool",
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/0/0c/Liverpool_FC.svg/1200px-Liverpool_FC.svg.png"
        },
        "predictions": {
            "home": "35%",
            "draw": "25%",
            "away": "40%"
        },
        "bothScore": "70%",
        "over2_5": "65%"
    },
    {
        "league": "La Liga",
        "countryFlag": "🇪🇸",
        "time": "17:00",
        "homeTeam": {
            "name": "Real Madrid",
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/5/56/Real_Madrid_CF.svg/1200px-Real_Madrid_CF.svg.png"
        },
        "awayTeam": {
            "name": "Barcelona",
            "logo": "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/FC_Barcelona_%28crest%29.svg/1200px-FC_Barcelona_%28crest%29.svg.png"
        },
        "predictions": {
            "home": "50%",
            "draw": "22%",
            "away": "28%"
        },
        "bothScore": "62%",
        "over2_5": "58%"
    }
]

# --- INJEÇÃO DE CSS E FONTES ---
# Aqui injetamos o CSS do Tailwind, a fonte do Google Fonts e o CSS customizado
# para o fundo e a barra de rolagem.
# Isso é o que vai estilizar nossos cards de HTML.
st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        .stApp {
            background-color: #111827; /* bg-gray-900 */
        }
        body {
            font-family: 'Inter', sans-serif;
        }
        /* Esconde a barra de menu do Streamlit e o footer */
        #MainMenu, footer {
            display: none;
        }
        /* Estilo para a barra de rolagem */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: #1f2937; }
        ::-webkit-scrollbar-thumb { background: #4b5563; border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: #6b7280; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO DA PÁGINA ---
# Usamos st.markdown para criar um cabeçalho centralizado com as classes do Tailwind.
st.markdown("""
    <div class="text-center mb-8">
        <h1 class="text-3xl md:text-4xl font-bold text-white">
            🤖 Jogos do Dia
        </h1>
        <p class="text-gray-400 mt-2">Análises e probabilidades dos principais jogos de hoje.</p>
    </div>
""", unsafe_allow_html=True)


# --- FUNÇÃO PARA CRIAR O CARD DE UM JOGO ---
# Esta função recebe um dicionário com os dados de um jogo e retorna uma string HTML formatada.
def create_match_card(match: dict) -> str:
    """Gera o HTML para um único card de jogo."""
    return f"""
        <div class="bg-gray-800 rounded-lg shadow-lg p-4 md:p-6 transition-transform transform hover:scale-[1.02] mb-4 max-w-4xl mx-auto">
            <!-- Cabeçalho do Card: Liga e País -->
            <div class="flex items-center justify-between pb-3 border-b border-gray-700">
                <div class="flex items-center space-x-3">
                    <span class="text-2xl">{match['countryFlag']}</span>
                    <span class="font-semibold text-white">{match['league']}</span>
                </div>
            </div>

            <!-- Detalhes da Partida: Times e Horário -->
            <div class="flex items-center justify-between my-4">
                <!-- Time da Casa -->
                <div class="flex flex-col items-center w-1/3 text-center">
                    <img src="{match['homeTeam']['logo']}" alt="Logo {match['homeTeam']['name']}" class="w-12 h-12 md:w-16 md:h-16 object-contain rounded-full mb-2">
                    <span class="font-bold text-sm md:text-base text-gray-200">{match['homeTeam']['name']}</span>
                </div>

                <!-- Horário e VS -->
                <div class="text-center">
                    <span class="text-xl md:text-2xl font-bold text-gray-400">{match['time']}</span>
                    <span class="text-xs text-gray-500 block">VS</span>
                </div>

                <!-- Time Visitante -->
                <div class="flex flex-col items-center w-1/3 text-center">
                    <img src="{match['awayTeam']['logo']}" alt="Logo {match['awayTeam']['name']}" class="w-12 h-12 md:w-16 md:h-16 object-contain rounded-full mb-2">
                    <span class="font-bold text-sm md:text-base text-gray-200">{match['awayTeam']['name']}</span>
                </div>
            </div>

            <!-- Seção de Probabilidades -->
            <div class="bg-gray-900/50 rounded-lg p-3 mt-4">
                <div class="grid grid-cols-3 gap-2 text-center text-xs md:text-sm">
                    <div class="bg-green-500/20 text-green-300 p-2 rounded-md">
                        <div class="font-bold text-lg">{match['predictions']['home']}</div>
                        <div class="font-semibold">CASA</div>
                    </div>
                    <div class="bg-yellow-500/20 text-yellow-300 p-2 rounded-md">
                        <div class="font-bold text-lg">{match['predictions']['draw']}</div>
                        <div class="font-semibold">EMPATE</div>
                    </div>
                    <div class="bg-red-500/20 text-red-300 p-2 rounded-md">
                        <div class="font-bold text-lg">{match['predictions']['away']}</div>
                        <div class="font-semibold">FORA</div>
                    </div>
                </div>
                <div class="grid grid-cols-2 gap-2 mt-2 text-center text-xs md:text-sm">
                     <div class="bg-blue-500/20 text-blue-300 p-2 rounded-md">
                        <div class="font-bold text-lg">{match['bothScore']}</div>
                        <div class="font-semibold">AMBAS MARCAM</div>
                    </div>
                    <div class="bg-purple-500/20 text-purple-300 p-2 rounded-md">
                        <div class="font-bold text-lg">{match['over2_5']}</div>
                        <div class="font-semibold">MAIS DE 2.5 GOLS</div>
                    </div>
                </div>
            </div>
            
            <!-- Botão de Ação (funcionalidade pode ser adicionada depois) -->
            <div class="mt-4">
                <a href="#" class="block w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-colors text-center no-underline">
                    Ver Análise Completa
                </a>
            </div>
        </div>
    """

# --- RENDERIZAÇÃO DOS CARDS ---
# Itera sobre a lista de jogos e renderiza um card para cada um.
if matches_data:
    for match in matches_data:
        html_card = create_match_card(match)
        st.markdown(html_card, unsafe_allow_html=True)
else:
    # Mensagem para quando não houver jogos
    st.markdown("""
        <div class="bg-gray-800 rounded-lg p-8 text-center text-gray-400 max-w-4xl mx-auto">
            <h3 class="text-xl font-semibold text-white">Nenhum jogo para hoje</h3>
            <p>Volte mais tarde para conferir as partidas do dia.</p>
        </div>
    """, unsafe_allow_html=True)

