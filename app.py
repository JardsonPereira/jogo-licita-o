import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Licitas-Minado Pro", page_icon="⚖️", layout="wide")

# 2. CSS Avançado para Interatividade
st.markdown("""
    <style>
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
    .status-card {
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        text-align: center;
    }
    .error-bg { background-color: #ffebee; border: 2px solid #ff1744; color: #b71c1c; }
    .success-bg { background-color: #e8f5e9; border: 2px solid #2e7d32; color: #1b5e20; }
    .win-bg { background-color: #fff9c4; border: 2px solid #fbc02d; color: #f57f17; }
    </style>
    """, unsafe_allow_html=True)

# 3. Definições de Conteúdo
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

# 4. Função de Inicialização
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
    if st.session_state.get('game_over') or st.session_state.get('vitoria'):
        return
    
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
    st.markdown("<h1 style='text-align: center;'>🕵️ Licitas-Minado Pro</h1>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        st.info("🎯 **Objetivo:** Analisar 25 pastas e encontrar os princípios da Nova Lei de Licitações.")
        st.warning("🚨 **Risco:** O campo contém irregularidades. Um erro anula sua auditoria!")
        if st.button("🚀 INICIAR AUDITORIA PROFISSIONAL"):
            preparar_tabuleiro()
            st.rerun()
else:
    st.markdown("<h2 style='text-align: center; color: #333;'>📁 Painel de Auditoria Digital</h2>", unsafe_allow_html=True)
    
    # Placar e Barra de Progresso (CORRIGIDA)
    pontuacao = st.session_state.get('score', 0)
    c_score, c_meta = st.columns(2)
    c_score.metric("📊 Integridade", f"{pontuacao} pts")
    
    # AQUI ESTAVA O ERRO DE SINTAXE - CORRIGIDO ABAIXO:
    progresso = min(pontuacao / 150, 1.0)
    c_meta.progress(progresso, text="Progresso da Homologação")

    # Banners de Feedback
    if st.session_state.get('game_over'):
        erro = st.session_state.get('erro_fatal', 'Erro Desconhecido')
        st.markdown(f"""<div class="status-card error-bg">
            <h3>💥 IMPUGNAÇÃO: {erro}</h3>
            <p>{ERROS_DETALHES.get(erro, "Irregularidade grave detectada.")}</p>
            </div>""", unsafe_allow_html=True)
        if st.button("🔄 Reiniciar Novo Processo"):
            preparar_tabuleiro()
            st.rerun()

    elif st.session_state.get('vitoria'):
        st.markdown("""<div class="status-card win-bg">
            <h3>🏆 CERTAME HOMOLOGADO!</h3>
            <p>Auditoria concluída com 100% de integridade.</p>
            </div>""", unsafe_allow_html=True)
        st.balloons()
        if st.button("🏗️ Iniciar Outra Licitação"):
            preparar_tabuleiro()
            st.rerun()

    elif st.session_state.get('ultimo_acerto'):
        acerto = st.session_state.get('ultimo_acerto')
        st.markdown(f"""<div class="status-card success-bg">
            <strong>✅ Princípio Validado: {acerto}</strong> - {PRINCIPIOS_DETALHES.get(acerto, "")}
            </div>""", unsafe_allow_html=True)

    # Grid de Pastas
    with st.container():
        for r in range(TAMANHO):
            cols = st.columns(TAMANHO)
            for c in range(TAMANHO):
                item = st.session_state['tabuleiro'][r][c]
                revelado = st.session_state['revelados'][r][c]
                
                if revelado:
                    if item in ERROS_DETALHES:
                        cols[c].markdown("<h1 style='text-align:center; margin:0;'>🚨</h1>", unsafe_allow_html=True)
                    elif item in PRINCIPIOS_DETALHES:
                        cols[c].markdown("<h1 style='text-align:center; margin:0;'>⚖️</h1>", unsafe_allow_html=True)
                    else:
                        cols[c].markdown("<h1 style='text-align:center; margin:0;'>📄</h1>", unsafe_allow_html=True)
                else:
                    if cols[c].button("📁", key=f"b{r}c{c}", disabled=st.session_state.get('game_over') or st.session_state.get('vitoria')):
                        clicar_casa(r, c)
                        st.rerun()

    # Barra Lateral
    with st.sidebar:
        st.title("📖 Suporte")
        st.info("⚖️ Princípios: 20 pts\n\n📄 Docs: 5 pts")
        if st.button("⏹️ Voltar ao Início"):
            st.session_state.clear()
            st.rerun()
