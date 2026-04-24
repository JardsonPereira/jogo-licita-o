import streamlit as st
import time
import random

# Configuração da Página
st.set_page_config(page_title="Licitas-Snake: O Jogo", layout="centered")

# --- ESTADO DO JOGO ---
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direcao = "DIREITA"
    st.session_state.documento = (random.randint(0, 9), random.randint(0, 9))
    st.session_state.pontos = 0
    st.session_state.game_over = False
    st.session_state.docs_coletados = []

# Itens temáticos para coletar
ITENS_LICITACAO = ["📄 Edital", "🆔 CNPJ", "📜 Certidão", "💰 Proposta", "✍️ Assinatura"]

def reiniciar():
    st.session_state.snake = [(5, 5), (5, 4), (5, 3)]
    st.session_state.direcao = "DIREITA"
    st.session_state.pontos = 0
    st.session_state.game_over = False
    st.session_state.docs_coletados = []
    st.session_state.documento = (random.randint(0, 9), random.randint(0, 9))

# --- INTERFACE ---
st.title("🪱 Licitas-Snake")
st.subheader("Colete os documentos para vencer a licitação!")

# Sidebar com placar
st.sidebar.header("📋 Status do Processo")
st.sidebar.metric("Pontos (Milhões R$)", st.session_state.pontos)
st.sidebar.write("### Documentos Coletados:")
for d in st.session_state.docs_coletados[-5:]: # Mostra os últimos 5
    st.sidebar.write(f"- {d}")

# Controles de direção
st.write("### 🎮 Controles")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("⬅️ Esquerda"): st.session_state.direcao = "ESQUERDA"
with col2:
    if st.button("⬆️ Cima"): st.session_state.direcao = "CIMA"
with col3:
    if st.button("⬇️ Baixo"): st.session_state.direcao = "BAIXO"
with col4:
    if st.button("➡️ Direita"): st.session_state.direcao = "DIREITA"

# --- LÓGICA DO MOVIMENTO ---
if not st.session_state.game_over:
    cabeca_x, cabeca_y = st.session_state.snake[0]

    if st.session_state.direcao == "CIMA": cabeca_x -= 1
    elif st.session_state.direcao == "BAIXO": cabeca_x += 1
    elif st.session_state.direcao == "ESQUERDA": cabeca_y -= 1
    elif st.session_state.direcao == "DIREITA": cabeca_y += 1

    nova_cabeca = (cabeca_x, cabeca_y)

    # Checar colisão com bordas ou corpo
    if (cabeca_x < 0 or cabeca_x >= 10 or cabeca_y < 0 or cabeca_y >= 10 
        or nova_cabeca in st.session_state.snake):
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, nova_cabeca)
        
        # Checar se coletou documento
        if nova_cabeca == st.session_state.documento:
            st.session_state.pontos += 10
            st.session_state.docs_coletados.append(random.choice(ITENS_LICITACAO))
            st.session_state.documento = (random.randint(0, 9), random.randint(0, 9))
            st.toast("Documento Coletado!", icon="📄")
        else:
            st.session_state.snake.pop()

# --- RENDERIZAÇÃO DO TABULEIRO ---
grid = [["⬜" for _ in range(10)] for _ in range(10)]

# Desenha o documento
dx, dy = st.session_state.documento
grid[dx][dy] = "📂"

# Desenha a minhoca
for i, (sx, sy) in enumerate(st.session_state.snake):
    if i == 0:
        grid[sx][sy] = "🪱" # Cabeça
    else:
        grid[sx][sy] = "🟩" # Corpo

# Exibe o grid
tabuleiro_texto = "\n".join([" ".join(linha) for linha in grid])
st.code(tabuleiro_texto, language="")

if st.session_state.game_over:
    st.error(f"💥 PROCESSO IMPUGNADO! Você bateu. Pontuação final: {st.session_state.pontos}")
    if st.button("Tentar Novamente"):
        reiniciar()
        st.rerun()

st.info("Dica: Clique no botão de direção e o Streamlit atualizará a posição. Cada '📂' é um documento para sua pasta de licitação.")
