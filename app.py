import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Licitas-Minado: Auditoria", page_icon="🕵️", layout="centered")

# 2. Estilo CSS para o Visual do Jogo
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; 
        height: 3.5em; 
        font-size: 20px; 
        font-weight: bold;
    }
    .error-container { 
        background-color: #ff4b4b; 
        color: white; 
        padding: 25px; 
        border-radius: 15px; 
        text-align: center; 
        margin-bottom: 20px;
        border: 2px solid #b22222;
    }
    .success-container {
        background-color: #28a745;
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Definições de Conteúdo
TAMANHO = 5
ERROS_DETALHES = {
    "Superfaturamento": "Os preços foram fixados muito acima do valor de mercado para desviar recursos públicos.",
    "Direcionamento": "O edital continha cláusulas restritivas que favoreciam apenas um licitante específico.",
    "Fraude": "Houve falsificação de documentos ou selos para burlar a legalidade do certame.",
    "Corrupção": "Identificou-se o oferecimento de vantagem indevida a agentes públicos envolvidos.",
    "Cartel": "Empresas concorrentes combinaram preços previamente para eliminar a disputa real."
}

PRINCIPIOS = ["Legalidade", "Impessoalidade", "Moralidade", "Publicidade", "Eficiência", "Isonomia", "Probidade"]

# 4. Inicialização do Estado do Jogo (session_state)
if 'tabuleiro' not in st.session_state:
    bombas = list(ERROS_DETALHES.keys())
    conteudo = PRINCIPIOS + bombas
    # Preenche o restante com documentos comuns
    while len(conteudo) < TAMANHO * TAMANHO:
        conteudo.append("Documento OK")
    
    random.shuffle(conteudo)
    
    # Organiza em matriz 5x5
    st.session_state.tabuleiro = [conteudo[i:i+TAMANHO] for i in range(0, len(conteudo), TAMANHO)]
    st.session_state.revelados = [[False for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.erro_fatal = ""
    st.session_state.vitoria = False

# 5. Lógica ao clicar na Pasta
def clicar_casa(r, c):
    if st.session_state.game_over or st.session_state.vitoria:
        return
    
    item = st.session_state.tabuleiro[r][c]
    st.session_state.revelados[r][c] = True
    
    if item in ERROS_DETALHES:
        st.session_state.game_over = True
        st.session_state.erro_fatal = item
    elif item in PRINCIPIOS:
        st.session_state.score += 20
    else:
        st.session_state.score += 5
    
    # Condição de Vitória (exemplo: atingir 100 pontos)
    if st.session_state.score >= 100:
        st.session_state.vitoria = True

# 6. Interface do Usuário (UI)
st.title("🕵️ Licitas-Minado: O Jogo")
st.write("Analise as pastas do processo licitatório. Acumule **Pontos de Integridade** encontrando princípios e documentos válidos, mas cuidado com as **Irregularidades**!")

# Painel de Game Over ou Vitória
if st.session_state.game_over:
    # Correção do erro de f-string:
    detalhe = ERROS_DETALHES.get(st.session_state.erro_fatal, "Irregularidade não identificada.")
    st.markdown(f"""
        <div class="error-container">
            <h2>💥 PROCESSO IMPUGNADO!</h2>
            <p>Você encontrou: <strong>{st.session_state.erro_fatal}</strong></p>
            <p style="font-size: 14px;">{detalhe}</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Nova Auditoria"):
        st.session_state.clear()
        st.rerun()

elif st.session_state.vitoria:
    st.markdown("""
        <div class="success-container">
            <h2>🏆 COMPLIANCE APROVADO!</h2>
            <p>Você atingiu o nível máximo de integridade no processo.</p>
        </div>
    """, unsafe_allow_html=True)
    st.balloons()
    if st.button("🚀 Iniciar Outro Pregão"):
        st.session_state.clear()
        st.rerun()

# Exibição do Score
st.metric("Pontos de Integridade", f"{st.session_state.score} pts")

st.divider()

# 7. Renderização da Grade de Pastas
for r in range(TAMANHO):
    cols = st.columns(TAMANHO)
    for c in range(TAMANHO):
        item = st.session_state.tabuleiro[r][c]
        revelado = st.session_state.revelados[r][c]
        
        if revelado:
            if item in ERROS_DETALHES:
                cols[c].button("🚨", key=f"btn-{r}-{c}", disabled=True)
            elif item in PRINCIPIOS:
                cols[c].button("⚖️", key=f"btn-{r}-{c}", help=f"Princípio da {item}", disabled=True)
            else:
                cols[c].button("📄", key=f"btn-{r}-{c}", disabled=True)
        else:
            # Botão clicável para revelar
            if cols[c].button("📁", key=f"btn-{r}-{c}", disabled=st.session_state.game_over or st.session_state.vitoria):
                clicar_casa(r, c)
                st.rerun()

# 8. Rodapé Informativo
st.divider()
st.info("💡 **Dica de Auditor:** Princípios (⚖️) valem 20 pontos. Documentos comuns (📄) valem 5 pontos. Sirenes (🚨) encerram o processo!")
