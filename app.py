import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Licitas-Minado", page_icon="🕵️")

# --- ESTILO CUSTOMIZADO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3em; font-size: 20px; }
    .status-box { padding: 20px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES DO JOGO ---
TAMANHO = 5
PRINCIPIOS = ["Legalidade", "Impessoalidade", "Moralidade", "Publicidade", "Eficiência", "Isonomia", "Probidade", "Planejamento"]
BOMBAS = ["Superfaturamento", "Direcionamento", "Fraude", "Corrupção", "Cartel"]

# --- INICIALIZAÇÃO DO ESTADO ---
if 'tabuleiro' not in st.session_state:
    # Criar tabuleiro misto
    conteudo = PRINCIPIOS + BOMBAS
    random.shuffle(conteudo)
    # Preencher o resto com "Documento Ok"
    while len(conteudo) < TAMANHO * TAMANHO:
        conteudo.append("Documento OK")
    random.shuffle(conteudo)
    
    st.session_state.tabuleiro = [conteudo[i:i+TAMANHO] for i in range(0, len(conteudo), TAMANHO)]
    st.session_state.revelados = [[False for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.vitoria = False

def clicar_casa(r, c):
    if st.session_state.game_over or st.session_state.vitoria:
        return
    
    st.session_state.revelados[r][c] = True
    item = st.session_state.tabuleiro[r][c]
    
    if item in BOMBAS:
        st.session_state.game_over = True
    elif item in PRINCIPIOS:
        st.session_state.score += 10
    else:
        st.session_state.score += 2

    # Checar vitória (se todos os princípios foram achados ou todas as casas seguras limpas)
    if st.session_state.score >= 100: # Exemplo de meta
        st.session_state.vitoria = True

# --- INTERFACE ---
st.title("🕵️ Licitas-Minado: Auditoria de Campo")
st.write("Clique nas pastas para encontrar os **Princípios da Administração**. Evite as **Irregularidades**!")

# Placar e Status
col_score, col_status = st.columns(2)
col_score.metric("Pontos de Integridade", st.session_state.score)

if st.session_state.game_over:
    st.error("💥 PROCESSO CANCELADO! Você clicou em uma Irregularidade Gravíssima.")
    if st.button("Reiniciar Auditoria"):
        st.session_state.clear()
        st.rerun()
elif st.session_state.vitoria:
    st.balloons()
    st.success("🏆 EXCELÊNCIA EM COMPLIANCE! Você limpou o processo com sucesso.")
    if st.button("Nova Licitação"):
        st.session_state.clear()
        st.rerun()

st.divider()

# --- RENDERIZAÇÃO DO TABULEIRO ---
for r in range(TAMANHO):
    cols = st.columns(TAMANHO)
    for c in range(TAMANHO):
        if st.session_state.revelados[r][c]:
            item = st.session_state.tabuleiro[r][c]
            # Estilização baseada no tipo de item revelado
            if item in BOMBAS:
                cols[c].button(f"💣", key=f"{r}-{c}", disabled=True)
            elif item in PRINCIPIOS:
                cols[c].button(f"⚖️", key=f"{r}-{c}", help=item, disabled=True)
                st.toast(f"Princípio Encontrado: {item}")
            else:
                cols[c].button(f"📄", key=f"{r}-{c}", disabled=True)
        else:
            # Casa ainda escondida
            if cols[c].button("📁", key=f"{r}-{c}"):
                clicar_casa(r, c)
                st.rerun()

# Legenda e Dicas
with st.expander("📖 Manual do Auditor"):
    st.write("""
    - **📁 Pasta Fechada**: Documento ainda não analisado.
    - **⚖️ Balança**: Princípio fundamental encontrado (+10 pontos).
    - **📄 Papel**: Trâmite legal comum (+2 pontos).
    - **💣 Bomba**: Irregularidade (Fim de jogo!).
    """)
