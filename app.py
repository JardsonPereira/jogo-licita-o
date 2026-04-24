import streamlit as st

# Configuração inicial da página
st.set_page_config(page_title="Simulador de Licitação", page_icon="🔨")

# Inicialização das variáveis de estado (Banco de dados temporário)
if 'lance_atual' not in st.session_state:
    st.session_state.lance_atual = 100.0
if 'vencedor' not in st.session_state:
    st.session_state.vencedor = "Nenhum"
if 'historico' not in st.session_state:
    st.session_state.historico = []

st.title("🔨 Simulador de Licitação Interativo")

# Sidebar para configurações do leilão
with st.sidebar:
    st.header("Configurações do Item")
    item_nome = st.text_input("Item para Leilão", value="Servidor Cloud Pro")
    if st.button("Reiniciar Leilão"):
        st.session_state.lance_atual = 100.0
        st.session_state.vencedor = "Nenhum"
        st.session_state.historico = []
        st.rerun()

# Layout Principal
col1, col2 = st.columns(2)

with col1:
    st.metric(label="Lance Atual", value=f"R$ {st.session_state.lance_atual:.2f}")
    st.info(f"🏆 Licitante na liderança: **{st.session_state.vencedor}**")

with col2:
    st.subheader("Dê o seu lance")
    nome_usuario = st.text_input("Seu Nome/Empresa", placeholder="Ex: Tech Solutions")
    novo_lance = st.number_input("Valor do Lance (R$)", min_value=st.session_state.lance_atual + 1.0, step=10.0)

    if st.button("Confirmar Lance"):
        if nome_usuario:
            st.session_state.lance_atual = novo_lance
            st.session_state.vencedor = nome_usuario
            st.session_state.historico.insert(0, f"{nome_usuario} ofertou R$ {novo_lance:.2f}")
            st.success("Lance registrado com sucesso!")
            st.balloons()
            st.rerun()
        else:
            st.error("Por favor, insira o nome da empresa.")

st.divider()

# Histórico de Lances
st.subheader("📜 Histórico de Lances")
if st.session_state.historico:
    for registro in st.session_state.historico:
        st.write(registro)
else:
    st.write("Nenhum lance registrado ainda.")
