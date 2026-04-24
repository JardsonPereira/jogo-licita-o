import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Licitas-Minado: Auditoria", page_icon="🕵️", layout="centered")

# 2. Estilo CSS
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-size: 20px; font-weight: bold; }
    .error-container { 
        background-color: #ff4b4b; color: white; padding: 25px; border-radius: 15px; 
        text-align: center; margin-bottom: 20px; border: 2px solid #b22222; 
    }
    .success-container {
        background-color: #28a745; color: white; padding: 25px; border-radius: 15px; 
        text-align: center; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Definições
TAMANHO = 5
ERROS_DETALHES = {
    "Superfaturamento": "Preços fixados acima do valor de mercado para desviar recursos.",
    "Direcionamento": "Edital com cláusulas que favorecem apenas um licitante.",
    "Fraude": "Falsificação de documentos ou selos.",
    "Corrupção": "Vantagem indevida a agentes públicos.",
    "Cartel": "Acordo entre empresas para fixar preços."
}
PRINCIPIOS = ["Legalidade", "Impessoalidade", "Moralidade", "Publicidade", "Eficiência", "Isonomia", "Probidade"]

# 4. Inicialização Segura do Estado
if 'tabuleiro' not in st.session_state:
    bombas = list(ERROS_DETALHES.keys())
    conteudo = PRINCIPIOS + bombas
    while len(conteudo) < TAMANHO * TAMANHO:
        conteudo.append("Documento OK")
    random.shuffle(conteudo)
    
    st.session_state['tabuleiro'] = [conteudo[i:i+TAMANHO] for i in range(0, len(conteudo), TAMANHO)]
    st.session_state['revelados'] = [[False for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    st.session_state['score'] = 0
    st.session_state['game_over'] = False
    st.session_state['vitoria'] = False
    st.session_state['erro_fatal'] = ""

# 5. Lógica de Clique
def clicar_casa(r, c):
    if st.session_state['game_over'] or st.session_state['vitoria']:
        return
    
    item = st.session_state['tabuleiro'][r][c]
    st.session_state['revelados'][r][c] = True
    
    if item in ERROS_DETALHES:
        st.session_state['game_over'] = True
        st.session_state['erro_fatal'] = item
    elif item in PRINCIPIOS:
        st.session_state['score'] += 20
    else:
        st.session_state['score'] += 5
    
    if st.session_state['score'] >= 100:
        st.session_state['vitoria'] = True

# 6. Interface
st.title("🕵️ Licitas-Minado: O Jogo")

# Verificação de Game Over com proteção contra AttributeError
if st.session_state.get('game_over'):
    nome_erro = st.session_state.get('erro_fatal', 'Erro desconhecido')
    detalhe = ERROS_DETALHES.get(nome_erro, "Irregularidade identificada no processo.")
    
    st.markdown(f"""
        <div class="error-container">
            <h2>💥 PROCESSO IMPUGNADO!</h2>
            <p>Você encontrou: <strong>{nome_erro}</strong></p>
            <p style="font-size: 14px;">{detalhe}</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔄 Reiniciar Nova Auditoria"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

elif st.session_state.get('vitoria'):
    st.markdown('<div class="success-container"><h2>🏆 COMPLIANCE APROVADO!</h2></div>', unsafe_allow_html=True)
    st.balloons()
    if st.button("🚀 Iniciar Outro Pregão"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

st.metric("Integridade", f"{st.session_state.get('score', 0)} pts")
st.divider()

# 7. Grid
for r in range(TAMANHO):
    cols = st.columns(TAMANHO)
    for c in range(TAMANHO):
        item = st.session_state['tabuleiro'][r][c]
        revelado = st.session_state['revelados'][r][c]
        
        if revelado:
            icon = "🚨" if item in ERROS_DETALHES else ("⚖️" if item in PRINCIPIOS else "📄")
            cols[c].button(icon, key=f"r{r}c{c}", disabled=True)
        else:
            if cols[c].button("📁", key=f"b{r}c{c}", disabled=st.session_state.get('game_over')):
                clicar_casa(r, c)
                st.rerun()
