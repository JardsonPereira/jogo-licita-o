import streamlit as st
import random
import json
import os

# 1. Configuração da Página
st.set_page_config(page_title="Licitas-Minado Pro", page_icon="⚖️", layout="wide")

# 2. Funções de Ranking
def carregar_ranking():
    if os.path.exists('ranking.json'):
        try:
            with open('ranking.json', 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def salvar_no_ranking(nome, pontos):
    ranking = carregar_ranking()
    ranking.append({"nome": nome, "pontos": pontos})
    ranking = sorted(ranking, key=lambda x: x['pontos'], reverse=True)[:5]
    with open('ranking.json', 'w') as f:
        json.dump(ranking, f)

# 3. CSS Avançado
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 4.5em; font-size: 24px !important; border-radius: 12px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); border-color: #007bff; }
    .status-card { padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; border: 2px solid #ddd; }
    .error-bg { background-color: #ffebee; border-color: #ff1744; color: #b71c1c; }
    .success-bg { background-color: #e8f5e9; border-color: #2e7d32; color: #1b5e20; }
    .leaderboard { background-color: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 5px; border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# 4. Dados
TAMANHO = 5
ERROS_DETALHES = {
    "Superfaturamento": "Preços fixados acima do mercado.",
    "Direcionamento": "Edital favorecendo licitante específico.",
    "Fraude": "Falsificação de documentos ou propostas.",
    "Corrupção": "Vantagem indevida a agentes públicos.",
    "Cartel": "Acordo entre empresas concorrentes.",
    "Sobrepreço": "Valor orçado superior ao mercado.",
    "Jogo de Planilha": "Manipulação de quantitativos."
}
PRINCIPIOS_DETALHES = {
    "Legalidade": "Atuar conforme a lei.", "Impessoalidade": "Tratamento igual para todos.",
    "Moralidade": "Ética e boa-fé.", "Publicidade": "Transparência total.",
    "Eficiência": "Melhor resultado, menor gasto.", "Isonomia": "Igualdade entre competidores.",
    "Probidade": "Honestidade pública.", "Planejamento": "Estudo prévio.",
    "Transparência": "Acesso fácil à informação.", "Segregação de Funções": "Divisão de tarefas.",
    "Vinculação ao Edital": "Seguir regras do edital.", "Julgamento Objetivo": "Critérios claros."
}

# 5. Lógica de Inicialização
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
    st.session_state['ranking_salvo'] = False
    st.session_state['ultimo_acerto'] = ""
    st.session_state['erro_fatal'] = ""
    st.session_state['jogo_iniciado'] = True

# --- FLUXO DE TELAS ---

# TELA DE LOGIN / INÍCIO
if 'jogo_iniciado' not in st.session_state or not st.session_state['jogo_iniciado']:
    st.markdown("<h1 style='text-align: center;'>🕵️ Licitas-Minado Pro</h1>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        nome_input = st.text_input("📝 Nome do Auditor / Empresa:", key="input_nome")
        if st.button("🚀 INICIAR AUDITORIA"):
            if nome_input:
                st.session_state['usuario'] = nome_input
                preparar_tabuleiro()
                st.rerun()
            else:
                st.warning("Insira seu nome para continuar.")
        
        st.write("---")
        st.subheader("🏆 Melhores Auditores")
        for i, r in enumerate(carregar_ranking()):
            st.markdown(f"<div class='leaderboard'>{i+1}º {r['nome']} - {r['pontos']} pts</div>", unsafe_allow_html=True)

# TELA DO JOGO
else:
    # Garantir que as chaves existam antes de renderizar (Prevenção de AttributeError)
    usuario = st.session_state.get('usuario', 'Auditor')
    pontuacao = st.session_state.get('score', 0)
    
    st.markdown(f"<h3 style='text-align: center;'>🛠️ Auditoria de: {usuario}</h3>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    c1.metric("📊 Pontos de Integridade", f"{pontuacao} pts")
    c2.progress(min(pontuacao / 150, 1.0), text="Meta de Homologação")

    # Fim do Jogo
    if st.session_state.get('game_over') or st.session_state.get('vitoria'):
        if not st.session_state.get('ranking_salvo', False):
            salvar_no_ranking(usuario, pontuacao)
            st.session_state['ranking_salvo'] = True

        if st.session_state.get('game_over'):
            erro = st.session_state.get('erro_fatal', 'Irregularidade')
            st.markdown(f'<div class="status-card error-bg"><h3>💥 PROCESSO IMPUGNADO!</h3><p>Causa: {erro} - {ERROS_DETALHES.get(erro, "")}</p></div>', unsafe_allow_html=True)
        else:
            st.balloons()
            st.markdown('<div class="status-card success-bg"><h3>🏆 CERTAME HOMOLOGADO COM SUCESSO!</h3></div>', unsafe_allow_html=True)
        
        if st.button("🔄 Voltar ao Menu"):
            st.session_state['jogo_iniciado'] = False
            st.rerun()

    # Grid de Jogo
    st.write("---")
    for r in range(TAMANHO):
        cols = st.columns(TAMANHO)
        for c in range(TAMANHO):
            # Acesso seguro ao tabuleiro e revelados
            tab = st.session_state.get('tabuleiro', [])
            rev = st.session_state.get('revelados', [])
            
            if tab and rev:
                item = tab[r][c]
                is_revelado = rev[r][c]
                
                if is_revelado:
                    icon = "🚨" if item in ERROS_DETALHES else ("⚖️" if item in PRINCIPIOS_DETALHES else "📄")
                    cols[c].button(icon, key=f"r{r}c{c}", disabled=True)
                else:
                    if cols[c].button("📁", key=f"b{r}c{c}", disabled=st.session_state.get('game_over') or st.session_state.get('vitoria')):
                        # Lógica de clique interna para evitar erros de escopo
                        st.session_state['revelados'][r][c] = True
                        if item in ERROS_DETALHES:
                            st.session_state['game_over'] = True
                            st.session_state['erro_fatal'] = item
                        elif item in PRINCIPIOS_DETALHES:
                            st.session_state['score'] += 20
                        else:
                            st.session_state['score'] += 5
                        if st.session_state['score'] >= 150:
                            st.session_state['vitoria'] = True
                        st.rerun()

    if st.sidebar.button("⚙️ Reset Geral"):
        st.session_state.clear()
        st.rerun()
