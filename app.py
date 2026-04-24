import streamlit as st
import random

# 1. Configuração da Página e Favicon
st.set_page_config(page_title="Licitas-Minado Pro", page_icon="⚖️", layout="wide")

# 2. CSS Avançado para Interatividade
st.markdown("""
    <style>
    /* Estilização dos botões/pastas */
    .stButton>button {
        width: 100%;
        height: 4.5em;
        font-size: 24px !important;
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        background-color: #ffffff;
    }
    .stButton>button:hover {
        border-color: #007bff;
        transform: translateY(-3px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Banners de feedback */
    .status-card {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
        animation: fadeIn 0.5s ease-in;
    }
    .error-bg { background-color: #ffebee; border: 2px solid #ff1744; color: #b71c1c; }
    .success-bg { background-color: #e8f5e9; border: 2px solid #2e7d32; color: #1b5e20; }
    .win-bg { background-color: #fff9c4; border: 2px solid #fbc02d; color: #f57f17; }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Definições de Conteúdo (Mantidas conforme solicitado)
TAMANHO = 5
ERROS_DETALHES = {
    "Superfaturamento": "Preços fixados acima do valor de mercado para desviar recursos.",
    "Direcionamento": "Edital com cláusulas que favorecem apenas um licitante específico.",
    "Fraude": "Falsificação de documentos, selos ou propostas.",
    "Corrupção": "Oferecimento ou promessa de vantagem indevida a agentes públicos.",
    "Cartel": "Acordo entre empresas para fixar preços e eliminar a concorrência.",
    "Sobrepreço": "Valor orçado para a licitação em valor expressivamente superior aos preços de mercado.",
    "Jogo de Planilha": "Alteração de quantitativos para beneficiar o licitante em prejuízo da administração."
}

PRINCIPIOS_DETALHES = {
    "Legalidade": "A administração deve atuar estritamente conforme a lei.",
    "Impessoalidade": "O tratamento deve ser igual para todos, sem favoritismos.",
    "Moralidade": "A atuação deve seguir padrões éticos, de probidade e boa-fé.",
    "Publicidade": "Transparência total dos atos para permitir o controle social.",
    "Eficiência": "Busca pelo melhor resultado com o menor gasto público possível.",
    "Isonomia": "Garantia de igualdade de condições a todos os competidores.",
    "Probidade": "Zelo, honestidade e integridade no trato com a coisa pública.",
    "Planejamento": "A licitação deve ser precedida de estudo técnico e planejamento.",
    "Transparência": "Acesso facilitado às informações do processo para qualquer cidadão.",
    "Segregação de Funções": "Divisão de tarefas para evitar que a mesma pessoa controle todas as etapas.",
    "Vinculação ao Edital": "As regras estabelecidas no edital devem ser seguidas rigorosamente.",
    "Julgamento Objetivo": "A escolha do vencedor deve seguir critérios claros e sem subjetividade."
}

# 4. Lógica de Inicialização
def preparar_tabuleiro():
    bombas = list(ERROS_DETALHES.keys())
    principios_sorteados = random.sample(list(PRINCIPIOS_DETALHES.keys()), 10)
    conteudo = principios_sorteados + bombas
    while len(conteudo) < TAMANHO * TAMANHO:
        conteudo.append("Documento OK")
    random.shuffle(conteudo)
    
    st.session_state['tabuleiro'] = [conteudo[i:i+TAMANHO] for i in range(0, len(conteudo), TAMANHO)]
    st.session_state['revelados'] = [[False for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    st.session_state['score'] = 0
    st.session_state['game_over'] = False
    st.session_state['vitoria'] = False
    st.session_state['ultimo_acerto'] = ""
    st.session_state['erro_fatal'] = ""
    st.session_state['jogo_iniciado'] = True

# 5. Lógica de Clique
def clicar_casa(r, c):
    item = st.session_state['tabuleiro'][r][c]
    st.session_state['revelados'][r][c] = True
    
    if item in ERROS_DETALHES:
        st.session_state['game_over'] = True
        st.session_state['erro_fatal'] = item
    elif item in PRINCIPIOS_DETALHES:
        st.session_state['score'] += 20
        st.session_state['ultimo_acerto'] = item
    else:
        st.session_state['score'] += 5
        st.session_state['ultimo_acerto'] = ""
    
    if st.session_state['score'] >= 150:
        st.session_state['vitoria'] = True

# --- FLUXO DE INTERFACE ---

if 'jogo_iniciado' not in st.session_state:
    # TELA DE START ESTILIZADA
    st.markdown("<h1 style='text-align: center;'>🕵️ Licitas-Minado Pro</h1>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.info("🎯 **Objetivo:** Analisar 25 pastas de um processo licitatório e encontrar os princípios da Lei 14.133/21.")
        st.warning("🚨 **Risco:** O Campo está minado com irregularidades. Um erro anula sua auditoria!")
        if st.button("🚀 INICIAR AUDITORIA PROFISSIONAL"):
            preparar_tabuleiro()
            st.rerun()
else:
    # Cabeçalho com Placar Estilizado
    st.markdown("<h2 style='text-align: center; color: #333;'>📁 Painel de Auditoria Digital</h2>", unsafe_allow_html=True)
    
    c_score, c_meta = st.columns(2)
    c_score.metric("📊 Integridade", f"{st.session_state['score']} pts")
    c_meta.progress(min(st.session_state['score'] / 150, 1.0), text
