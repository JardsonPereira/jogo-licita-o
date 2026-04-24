import streamlit as st
import random

# Configuração da página
st.set_page_config(page_title="Licitas-Snake 2.0", page_icon="🏗️")

# --- CSS PARA MELHORAR O VISUAL ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #f0f2f6; }
    .game-container { line-height: 1.2; font-size: 25px; text-align: center; background: #1e1e1e; padding: 20px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- INICIALIZAÇÃO DO ESTADO ---
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'snake' not in st.session_state:
    st.session_state.snake = [(5, 5), (5, 4)]
if 'direcao' not in st.session_state:
    st.session_state.direcao = "DIREITA"
if 'documento' not in st.session_state:
    st.session_state.documento = (3, 3)
if 'pontos' not in st.session_state:
    st.session_state.pontos = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Lista de itens que valem pontos
ITENS = ["📄", "📜", "📂", "🖋️", "⚖️", "💰"]

def reiniciar_jogo():
    st.session_state.snake = [(5, 5), (5, 4)]
    st.session_state.direcao = "DIREITA"
    st.session_state.pontos = 0
    st.session_state.game_over = False
    st.session_state.game_started = True

# --- TELA INICIAL ---
if not st.session_state.game_started:
    st.title("🏗️ Licitas-Snake: O Jogo")
    st.write("Sua missão é coletar todos os documentos e propostas para vencer o contrato público.")
    st.info("Regras: Use os botões para guiar a minhoca. Não bata nas bordas nem em si mesmo!")
    if st.button("🚀 INICIAR LICITAÇÃO"):
        st.session_state.game_started = True
        st.rerun()

# --- JOGO ATIVO ---
else:
    st.title("🪱 Processo em Andamento...")
    
    # Colunas de Status
    col_score, col_status = st.columns(2)
    col_score.metric("Pontos Acumulados", f"{st.session_state.pontos}")
    
    if st.session_state.game_over:
        st.error("💥 PROCESSO IMPUGNADO! Você cometeu um erro jurídico.")
        if st.button("Tentar Novamente"):
            reiniciar_jogo()
            st.rerun()
    else:
        # Controles
        st.write("### Direcione sua Proposta:")
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("⬆️"): st.session_state.direcao = "CIMA"
        if c2.button("⬇️"): st.session_state.direcao = "BAIXO"
        if c3.button("⬅️"): st.session_state.direcao = "ESQUERDA"
        if c4.button("➡️"): st.session_state.direcao = "DIREITA"

        # Lógica de Movimento
        cabeca_x, cabeca_y = st.session_state.snake[0]
        if st.session_state.direcao == "CIMA": cabeca_x -= 1
        elif st.session_state.direcao == "BAIXO": cabeca_x += 1
        elif st.session_state.direcao == "ESQUERDA": cabeca_y -= 1
        elif st.session_state.direcao == "DIREITA": cabeca_y += 1

        nova_cabeca = (cabeca_x, cabeca_y)

        # Verificação de Colisão
        if (cabeca_x < 0 or cabeca_x >= 10 or cabeca_y < 0 or cabeca_y >= 10 
            or nova_cabeca in st.session_state.snake):
            st.session_state.game_over = True
            st.rerun()
        else:
            st.session_state.snake.insert(0, nova_cabeca)
            if nova_cabeca == st.session_state.documento:
                st.session_state.pontos += 10
                st.session_state.documento = (random.randint(0, 9), random.randint(0, 9))
                st.toast("Documento Anexado!", icon="📎")
            else:
                st.session_state.snake.pop()

        # --- RENDERIZAÇÃO VISUAL ---
        grid = [["⬛" for _ in range(10)] for _ in range(10)]
        
        # Desenha Documento
        grid[st.session_state.documento[0]][st.session_state.documento[1]] = random.choice(ITENS)
        
        # Desenha a Minhoca com visual novo
        for i, (sx, sy) in enumerate(st.session_state.snake):
            if i == 0:
                grid[sx][sy] = "👷" # Cabeça (O Licitante)
            else:
                grid[sx][sy] = "🟦" # Corpo (O Processo)

        # Exibição estilizada
        board_html = "".join(["".join(row) + "<br>" for row in grid])
        st.markdown(f'<div class="game-container">{board_html}</div>', unsafe_allow_html=True)
        
        st.caption("Cada clique em uma seta move o processo um passo adiante.")

# Botão de Reset Permanente no Sidebar
if st.sidebar.button("Reset Geral"):
    st.session_state.clear()
    st.rerun()
