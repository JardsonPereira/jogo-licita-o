import streamlit as st
import random
import time

# Configuração da página
st.set_page_config(page_title="Leilão Tycoon", page_icon="🎮")

# --- INICIALIZAÇÃO DO ESTADO DO JOGO ---
if 'carteira' not in st.session_state:
    st.session_state.carteira = 5000.0
if 'inventario' not in st.session_state:
    st.session_state.inventario = []
if 'lance_atual' not in st.session_state:
    st.session_state.lance_atual = 0.0
if 'vencedor_atual' not in st.session_state:
    st.session_state.vencedor_atual = "Ninguém"
if 'item_atual' not in st.session_state:
    st.session_state.item_atual = {"nome": "Quadro Antigo", "base": 500.0}
if 'log' not in st.session_state:
    st.session_state.log = []
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- LÓGICA DOS BOTS ---
def lance_do_bot():
    # Bots só dão lance se não forem os vencedores atuais
    if st.session_state.vencedor_atual != "Bot Estratégico":
        limite_bot = st.session_state.item_atual["base"] * 2.5
        if st.session_state.lance_atual < limite_bot:
            incremento = random.choice([50, 100, 150])
            st.session_state.lance_atual += incremento
            st.session_state.vencedor_atual = "Bot Estratégico"
            st.session_state.log.insert(0, f"🤖 Bot deu um lance de R$ {st.session_state.lance_atual}")

# --- INTERFACE ---
st.title("🎮 Leilão Tycoon: O Jogo")

# Status do Jogador
st.sidebar.header("👤 Perfil do Jogador")
st.sidebar.metric("Sua Carteira", f"R$ {st.session_state.carteira:.2f}")
st.sidebar.subheader("📦 Seus Itens")
for item in st.session_state.inventario:
    st.sidebar.write(f"- {item}")

if not st.session_state.game_over:
    st.header(f"Item em leilão: {st.session_state.item_atual['nome']}")
    st.subheader(f"Preço Base: R$ {st.session_state.item_atual['base']:.2f}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Lance Mais Alto", f"R$ {st.session_state.lance_atual:.2f}", 
                  delta=f"Vencedor: {st.session_state.vencedor_atual}", delta_color="normal")
    
    with col2:
        novo_lance = st.number_input("Quanto deseja oferecer?", 
                                     min_value=st.session_state.lance_atual + 10.0, 
                                     step=50.0)
        
        if st.button("🔨 DAR LANCE!"):
            if novo_lance <= st.session_state.carteira:
                st.session_state.lance_atual = novo_lance
                st.session_state.vencedor_atual = "Você"
                st.session_state.log.insert(0, f"✅ Você deu um lance de R$ {novo_lance}")
                # Simular reação imediata do bot
                time.sleep(0.5)
                lance_do_bot()
                st.rerun()
            else:
                st.error("Dinheiro insuficiente!")

    # Botões de ação do jogo
    if st.button("Finalizar e Reivindicar"):
        if st.session_state.vencedor_atual == "Você":
            st.success(f"Parabéns! Você comprou o {st.session_state.item_atual['nome']}!")
            st.session_state.carteira -= st.session_state.lance_atual
            st.session_state.inventario.append(st.session_state.item_atual['nome'])
            st.balloons()
        else:
            st.error("Você não é o vencedor atual!")
        
        # Próximo item
        st.session_state.item_atual = random.choice([
            {"nome": "Vaso da Dinastia Ming", "base": 1200.0},
            {"nome": "Primeira Edição HQ", "base": 300.0},
            {"nome": "Carro Clássico 1960", "base": 3000.0}
        ])
        st.session_state.lance_atual = st.session_state.item_atual["base"]
        st.session_state.vencedor_atual = "Ninguém"
        st.rerun()

    # Log de Eventos
    st.divider()
    st.subheader("📝 Histórico da Rodada")
    for msg in st.session_state.log[:5]:
        st.write(msg)

else:
    st.error("Fim de Jogo!")
    if st.button("Reiniciar"):
        st.session_state.clear()
        st.rerun()
