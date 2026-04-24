import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Licitas-Minado: Auditoria", page_icon="🕵️")

# --- ESTILO ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-size: 18px; }
    .error-container { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 10px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÕES ---
TAMANHO = 5
# Dicionário de erros para dar contexto educativo
ERROS_DETALHES = {
    "Superfaturamento": "Preço fixado muito acima do valor de mercado para desviar verba.",
    "Direcionamento": "Edital feito com exigências que só uma empresa específica consegue cumprir.",
    "Fraude": "Falsificação de documentos ou selos para ganhar a disputa ilegalmente.",
    "Corrupção": "Oferecimento de vantagem indevida a agente público.",
    "Cartel": "Acordo entre empresas concorrentes para fixar preços e dividir o mercado."
}

PRINCIPIOS = ["Legalidade", "Impessoalidade", "Moralidade", "Publicidade", "Eficiência", "Isonomia", "Probidade"]

# --- ESTADO DO JOGO ---
if 'tabuleiro' not in st.session_state:
    bombas = list(ERROS_DETALHES.keys())
    conteudo = PRINCIPIOS + bombas
    while len(conteudo) < TAMANHO * TAMANHO:
        conteudo.append("Documento OK")
    random.shuffle(conteudo)
    
    st.session_state.tabuleiro = [conteudo[i:i+TAMANHO] for i in range(0, len(conteudo), TAMANHO)]
    st.session_state.revelados = [[False for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.erro_fatal = ""

def clicar_casa(r, c):
    item = st.session_state.tabuleiro[r][c]
    st.session_state.revelados[r][c] = True
    
    if item in ERROS_DETALHES:
        st.session_state.game_over = True
        st.session_state.erro_fatal = item
    elif item in PRINCIPIOS:
        st.session_state.score += 15
    else:
        st.session_state.score += 5

# --- INTERFACE ---
st.title("🕵️ Licitas-Minado")

# Exibição de Erro Fatal (Game Over)
if st.session_state.game_over:
    st.markdown(f"""
        <div class="error-container">
            <h2>💥 PROCESSO IMPUGNADO!</h2>
            <p>Você encontrou uma irregularidade: <strong>{st.session_state.erro_fatal}</strong></p>
            <small>{ERROS_DETALHES[st.session_state.erro_fatal]}</small>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Auditoria"):
        st.session_state.clear()
        st.rerun()

# Placar
st.metric("Pontos de Integridade", st.session_state.score)

# --- RENDERIZAÇÃO DO TABULEIRO ---
for r in range(TAMANHO):
    cols = st.columns(TAMANHO)
    for c in range(TAMANHO):
        item = st.session_state.tabuleiro[r][c]
        revelado = st.session_state.revelados[r][c]
        
        if revelado:
            if item in ERROS_DETALHES:
                cols[c].button("🚨", key=f"b-{r}-{c}", disabled=True)
            elif item in PRINCIPIOS:
                cols[c].button("⚖️", key=f"p-{r}-{c}", help=item, disabled=True)
            else:
                cols[c].button("📄", key=f"d-{r}-{c}", disabled=True)
        else:
            if cols[c].button("📁", key=f"f-{r}-{c}", disabled=st.session_state.game_over):
                clicar_casa(r, c)
                st.rerun()

st.divider()
st.info("Objetivo: Encontre os princípios (⚖️) e documentos (📄). Evite as irregularidades (🚨)!")
