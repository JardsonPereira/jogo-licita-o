import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Licitas-Minado: Auditoria", page_icon="🕵️", layout="centered")

# 2. Estilo CSS Customizado
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-size: 20px; font-weight: bold; }
    .error-container { 
        background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; 
        text-align: center; margin-bottom: 20px; border: 2px solid #b22222; 
    }
    .success-info {
        background-color: #28a745; color: white; padding: 15px; border-radius: 10px;
        text-align: center; margin-bottom: 20px; border: 1px solid #1e7e34;
    }
    .win-container {
        background-color: #ffc107; color: black; padding: 25px; border-radius: 15px;
        text-align: center; margin-bottom: 20px; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Definições de Conteúdo Educativo
TAMANHO = 5

ERROS_DETALHES = {
    "Superfaturamento": "Preços fixados acima do valor de mercado para desviar recursos.",
    "Direcionamento": "Edital com cláusulas que favorecem apenas um licitante específico.",
    "Fraude": "Falsificação de documentos, selos ou propostas.",
    "Corrupção": "Oferecimento ou promessa de vantagem indevida a agentes públicos.",
    "Cartel": "Acordo entre empresas para fixar preços e eliminar a concorrência."
}

PRINCIPIOS_DETALHES = {
    "Legalidade": "A administração deve atuar estritamente conforme a lei.",
    "Impessoalidade": "O tratamento deve ser igual para todos, sem favoritismos.",
    "Moralidade": "A atuação deve seguir padrões éticos e de boa-fé.",
    "Publicidade": "Transparência total dos atos para controle social.",
    "Eficiência": "Busca pelo melhor resultado com o menor gasto público.",
    "Isonomia": "Garantia de igualdade de condições a todos os concorrentes.",
    "Probidade": "Zelo com a coisa pública e honestidade administrativa."
}

# 4. Inicialização Segura do Estado
if 'tabuleiro' not in st.session_state:
    bombas = list(ERROS_DETALHES.keys())
    principios = list(PRINCIPIOS_DETALHES.keys())
    conteudo = principios + bombas
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

# 5. Lógica de Clique
def clicar_casa(r, c):
    if st.session_state.get('game_over') or st.session_state.get('vitoria'):
        return
    
    item = st.session_state['tabuleiro'][r][c]
    st.session_state['revelados'][r][c] = True
    
    if item in ERROS_DETALHES:
        st.session_state['game_over'] = True
        st.session_state['erro_fatal'] = item
        st.session_state['ultimo_acerto'] = ""
    elif item in PRINCIPIOS_DETALHES:
        st.session_state['score'] += 20
        st.session_state['ultimo_acerto'] = item
    else:
        st.session_state['score'] += 5
        st.session_state['ultimo_acerto'] = "" # Documento comum não mostra banner
    
    if st.session_state['score'] >= 120: # Meta para vencer
        st.session_state['vitoria'] = True

# 6. Interface do Usuário
st.title("🕵️ Licitas-Minado: Auditoria")

# BANNER DE ERRO (GAME OVER)
if st.session_state.get('game_over'):
    nome_erro = st.session_state.get('erro_fatal', 'Erro')
    desc_erro = ERROS_DETALHES.get(nome_erro, "")
    st.markdown(f"""
        <div class="error-container">
            <h2>💥 PROCESSO IMPUGNADO!</h2>
            <p>Irregularidade: <strong>{nome_erro}</strong></p>
            <small>{desc_erro}</small>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Reiniciar Auditoria"):
        st.session_state.clear()
        st.rerun()

# BANNER DE ACERTO (PRINCÍPIO ENCONTRADO)
elif st.session_state.get('ultimo_acerto'):
    nome_acerto = st.session_state.get('ultimo_acerto')
    desc_acerto = PRINCIPIOS_DETALHES.get(nome_acerto, "")
    st.markdown(f"""
        <div class="success-info">
            <h4>✅ Princípio de {nome_acerto}</h4>
            <p>{desc_acerto}</p>
        </div>
    """, unsafe_allow_html=True)

# BANNER DE VITÓRIA
if st.session_state.get('vitoria'):
    st.markdown('<div class="win-container"><h2>🏆 AUDITORIA CONCLUÍDA COM SUCESSO!</h2></div>', unsafe_allow_html=True)
    st.balloons()
    if st.button("🚀 Nova Licitação"):
        st.session_state.clear()
        st.rerun()

st.metric("Pontos de Integridade", f"{st.session_state.get('score', 0)} / 120")

# 7. Grid de Pastas
st.write("---")
for r in range(TAMANHO):
    cols = st.columns(TAMANHO)
    for c in range(TAMANHO):
        item = st.session_state['tabuleiro'][r][c]
        revelado = st.session_state['revelados'][r][c]
        
        if revelado:
            if item in ERROS_DETALHES:
                icon = "🚨"
            elif item in PRINCIPIOS_DETALHES:
                icon = "⚖️"
            else:
                icon = "📄"
            cols[c].button(icon, key=f"r{r}c{c}", disabled=True)
        else:
            if cols[c].button("📁", key=f"b{r}c{c}", disabled=st.session_state.get('game_over')):
                clicar_casa(r, c)
                st.rerun()

st.caption("Dica: Encontre as balanças (⚖️) para aprender os princípios e pontuar mais rápido!")
