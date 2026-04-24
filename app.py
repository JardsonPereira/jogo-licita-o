import streamlit as st
import random

# 1. Configuração da Página
st.set_page_config(page_title="Licitas-Minado: Auditoria 2.0", page_icon="🕵️", layout="centered")

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

# 3. Definições de Conteúdo Educativo (Expandido)
TAMANHO = 5

ERROS_DETALHES = {
    "Superfaturamento": "Preços fixados acima do valor de mercado para desviar recursos.",
    "Direcionamento": "Edital com cláusulas que favorecem apenas um licitante específico.",
    "Fraude": "Falsificação de documentos, selos ou propostas.",
    "Corrupção": "Oferecimento ou promessa de vantagem indevida a agentes públicos.",
    "Cartel": "Acordo entre empresas para fixar preços e eliminar a concorrência.",
    "Sobrepreço": "Valor orçado para a licitação em valor expressivamente superior aos preços de mercado.",
    "Jogo de Planilha": "Alteração de quantitativos para beneficiar o licitante em prejuízo da administração."
}

PRINCIPIOS_DETALHES = {
    "Legalidade": "A administração deve atuar estritamente conforme a lei.",
    "Impessoalidade": "O tratamento deve ser igual para todos, sem favoritismos.",
    "Moralidade": "A atuação deve seguir padrões éticos, de probidade e boa-fé.",
    "Publicidade": "Transparência total dos atos para permitir o controle social.",
    "Eficiência": "Busca pelo melhor resultado com o menor gasto público possível.",
    "Isonomia": "Garantia de igualdade de condições a todos os competidores.",
    "Probidade": "Zelo, honestidade e integridade no trato com a coisa pública.",
    "Planejamento": "A licitação deve ser precedida de estudo técnico e planejamento.",
    "Transparência": "Acesso facilitado às informações do processo para qualquer cidadão.",
    "Segregação de Funções": "Divisão de tarefas para evitar que a mesma pessoa controle todas as etapas.",
    "Vinculação ao Edital": "As regras estabelecidas no edital devem ser seguidas rigorosamente.",
    "Julgamento Objetivo": "A escolha do vencedor deve seguir critérios claros e sem subjetividade."
}

# 4. Função para Iniciar/Reiniciar e Embaralhar
def preparar_tabuleiro():
    bombas = list(ERROS_DETALHES.keys())
    # Sorteia uma quantidade de princípios para caber no tabuleiro mantendo o desafio
    principios_sorteados = random.sample(list(PRINCIPIOS_DETALHES.keys()), 10)
    
    conteudo = principios_sorteados + bombas
    while len(conteudo) < TAMANHO * TAMANHO:
        conteudo.append("Documento OK")
    
    # Embaralhamento garantido
    random.shuffle(conteudo)
    
    st.session_state['tabuleiro'] = [conteudo[i:i+TAMANHO] for i in range(0, len(conteudo), TAMANHO)]
    st.session_state['revelados'] = [[False for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    st.session_state['score'] = 0
    st.session_state['game_over'] = False
    st.session_state['vitoria'] = False
    st.session_state['ultimo_acerto'] = ""
    st.session_state['erro_fatal'] = ""

# Inicialização na primeira carga
if 'tabuleiro' not in st.session_state:
    preparar_tabuleiro()

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
        st.session_state['ultimo_acerto'] = ""
    
    if st.session_state['score'] >= 150: # Aumentei a meta para 150 pela maior gama de princípios
        st.session_state['vitoria'] = True

# 6. Interface do Usuário
st.title("🕵️ Licitas-Minado: Auditoria")
st.write("Analise o processo. Encontre os princípios da Lei 14.133/21 e evite as ilegalidades!")

# FEEDBACKS (ERROR / SUCCESS / WIN)
if st.session_state.get('game_over'):
    nome_erro = st.session_state.get('erro_fatal', 'Erro')
    st.markdown(f"""
        <div class="error-container">
            <h2>💥 PROCESSO IMPUGNADO!</h2>
            <p>Irregularidade: <strong>{nome_erro}</strong></p>
            <small>{ERROS_DETALHES.get(nome_erro, "")}</small>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 Reiniciar e Embaralhar"):
        preparar_tabuleiro()
        st.rerun()

elif st.session_state.get('ultimo_acerto'):
    nome_acerto = st.session_state.get('ultimo_acerto')
    st.markdown(f"""
        <div class="success-info">
            <h4>✅ Princípio: {nome_acerto}</h4>
            <p>{PRINCIPIOS_DETALHES.get(nome_acerto, "")}</p>
        </div>
    """, unsafe_allow_html=True)

if st.session_state.get('vitoria'):
    st.markdown('<div class="win-container"><h2>🏆 AUDITORIA DE EXCELÊNCIA!</h2><p>Processo 100% íntegro.</p></div>', unsafe_allow_html=True)
    st.balloons()
    if st.button("🚀 Novo Certame"):
        preparar_tabuleiro()
        st.rerun()

st.metric("Integridade do Processo", f"{st.session_state.get('score', 0)} / 150 pts")

# 7. Grid de Pastas
st.write("---")
for r in range(TAMANHO):
    cols = st.columns(TAMANHO)
    for c in range(TAMANHO):
        item = st.session_state['tabuleiro'][r][c]
        revelado = st.session_state['revelados'][r][c]
        
        if revelado:
            icon = "🚨" if item in ERROS_DETALHES else ("⚖️" if item in PRINCIPIOS_DETALHES else "📄")
            cols[c].button(icon, key=f"r{r}c{c}", disabled=True)
        else:
            if cols[c].button("📁", key=f"b{r}c{c}", disabled=st.session_state.get('game_over') or st.session_state.get('vitoria')):
                clicar_casa(r, c)
                st.rerun()

st.info("💡 Foram adicionados novos princípios como Segregação de Funções e Planejamento. Boa sorte, Auditor!")
