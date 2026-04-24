import streamlit as st
import random
import json
import os

# 1. Configuração da Página
st.set_page_config(page_title="Licitas-Minado Pro", page_icon="⚖️", layout="wide")

# 2. Funções de Ranking (Salva em arquivo JSON local)
def carregar_ranking():
    if os.path.exists('ranking.json'):
        with open('ranking.json', 'r') as f:
            return json.load(f)
    return []

def salvar_no_ranking(nome, pontos):
    ranking = carregar_ranking()
    ranking.append({"nome": nome, "pontos": pontos})
    # Ordena do maior para o menor e pega os top 5
    ranking = sorted(ranking, key=lambda x: x['pontos'], reverse=True)[:5]
    with open('ranking.json', 'w') as f:
        json.dump(ranking, f)

# 3. CSS Avançado
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 4.5em; font-size: 24px !important; border-radius: 12px; }
    .status-card { padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 20px; }
    .error-bg { background-color: #ffebee; border: 2px solid #ff1744; color: #b71c1c; }
    .success-bg { background-color: #e8f5e9; border: 2px solid #2e7d32; color: #1b5e20; }
    .leaderboard { background-color: #f8f9fa; padding: 15px; border-radius: 10px; border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# 4. Definições de Conteúdo
TAMANHO = 5
ERROS_DETALHES = {
    "Superfaturamento": "Preços fixados acima do valor de mercado.",
    "Direcionamento": "Edital com cláusulas que favorecem um licitante específico.",
    "Fraude": "Falsificação de documentos ou propostas.",
    "Corrupção": "Vantagem indevida a agentes públicos.",
    "Cartel": "Acordo entre empresas para fixar preços.",
    "Sobrepreço": "Valor orçado expressivamente superior ao mercado.",
    "Jogo de Planilha": "Alteração de quantitativos para beneficiar o licitante."
}

PRINCIPIOS_DETALHES = {
    "Legalidade": "Atuação estritamente conforme a lei.",
    "Impessoalidade": "Tratamento igual para todos, sem favoritismos.",
    "Moralidade": "Padrões éticos, de probidade e boa-fé.",
    "Publicidade": "Transparência total dos atos.",
    "Eficiência": "Melhor resultado com o menor gasto.",
    "Isonomia": "Igualdade de condições aos competidores.",
    "Probidade": "Zelo e honestidade com a coisa pública.",
    "Planejamento": "Estudo técnico e planejamento prévio.",
    "Transparência": "Acesso facilitado às informações.",
    "Segregação de Funções": "Divisão de tarefas para evitar fraudes.",
    "Vinculação ao Edital": "Regras do edital seguidas rigorosamente.",
    "Julgamento Objetivo": "Critérios claros e sem subjetividade."
}

# 5. Funções de Jogo
def preparar_tabuleiro():
    bombas = list(ERROS_DETALHES.keys())
    principios_sorteados = random.sample(list(PRINCIPIOS_DETALHES.keys()), 10)
    conteudo = principios_sorteados + bombas
    while len(conteudo) < TAMANHO * TAMANHO:
        conteudo.append("Documento OK")
    random.shuffle(conteudo)
    
    st.session_state['tabuleiro'] = [conteudo[i:i+TAMANHO] for i in range(0, len(conteudo), TAMANHO)]
    st.session_state['revelados'] = [[False for _ in range(TAMANHO)] for _ in range(TAMANHO)]
    st.session_state['score'] = 0
    st.session_state['game_over'] = False
    st.session_state['vitoria'] = False
    st.session_state['ranking_salvo'] = False
    st.session_state['ultimo_acerto'] = ""
    st.session_state['jogo_iniciado'] = True

def clicar_casa(r, c):
    item = st.session_state['tabuleiro'][r][c]
    st.session_state['revelados'][r][c] = True
    if item in ERROS_DETALHES:
        st.session_state['game_over'] = True
    elif item in PRINCIPIOS_DETALHES:
        st.session_state['score'] += 20
        st.session_state['ultimo_acerto'] = item
    else:
        st.session_state['score'] += 5
    if st.session_state['score'] >= 150:
        st.session_state['vitoria'] = True

# --- INTERFACE ---

if 'jogo_iniciado' not in st.session_state:
    st.markdown("<h1 style='text-align: center;'>🕵️ Licitas-Minado Pro</h1>", unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        nome = st.text_input("📝 Digite seu nome ou Empresa:", placeholder="Ex: Auditor 007")
        if st.button("🚀 INICIAR AUDITORIA"):
            if nome:
                st.session_state['usuario'] = nome
                preparar_tabuleiro()
                st.rerun()
            else:
                st.error("Por favor, digite seu nome para começar!")
        
        st.write("---")
        st.subheader("🏆 Top 5 Auditores")
        for i, r in enumerate(carregar_ranking()):
            st.markdown(f"<div class='leaderboard'>{i+1}º {r['nome']} - {r['pontos']} pts</div>", unsafe_allow_html=True)

else:
    st.markdown(f"<h3 style='text-align: center;'>Auditor em campo: {st.session_state['usuario']}</h3>", unsafe_allow_html=True)
    
    # Placar e Progresso
    pontuacao = st.session_state.get('score', 0)
    c1, c2 = st.columns(2)
    c1.metric("📊 Integridade", f"{pontuacao} pts")
    c2.progress(min(pontuacao / 150, 1.0), text="Meta de Homologação")

    # Final do Jogo
    if st.session_state.get('game_over') or st.session_state.get('vitoria'):
        # Salva no ranking apenas uma vez por rodada
        if not st.session_state.get('ranking_salvo'):
            salvar_no_ranking(st.session_state['usuario'], pontuacao)
            st.session_state['ranking_salvo'] = True

        if st.session_state['game_over']:
            st.markdown(f'<div class="status-card error-bg"><h3>💥 PROCESSO IMPUGNADO! Final: {pontuacao} pts</h3></div>', unsafe_allow_html=True)
        else:
            st.balloons()
            st.markdown('<div class="status-card success-bg"><h3>🏆 CERTAME HOMOLOGADO! Perfeito!</h3></div>', unsafe_allow_html=True)
        
        if st.button("🔄 Voltar ao Menu Principal"):
            st.session_state.clear()
            st.rerun()

    # Grid
    for r in range(TAMANHO):
        cols = st.columns(TAMANHO)
        for c in range(TAMANHO):
            item = st.session_state['tabuleiro'][r][c]
            revelado = st.session_state['revelados'][r][c]
            if revelado:
                icon = "🚨" if item in ERROS_DETALHES else ("⚖️" if item in PRINCIPIOS_DETALHES else "📄")
                cols[c].button(icon, key=f"r{r}c{c}", disabled=True)
            else:
                if cols[c].button("📁", key=f"b{r}c{c}", disabled=st.session_state['game_over'] or st.session_state['vitoria']):
                    clicar_casa(r, c)
                    st.rerun()
