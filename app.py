import time

def jogar_licitacao():
    pontuacao = 0
    perguntas = [
        {
            "pergunta": "Qual modalidade é obrigatória para aquisição de bens e serviços comuns?",
            "opcoes": ["A) Concorrência", "B) Pregão", "C) Diálogo Competitivo", "D) Leilão"],
            "resposta": "B"
        },
        {
            "pergunta": "Na nova lei, qual critério de julgamento NÃO é permitido?",
            "opcoes": ["A) Menor Preço", "B) Técnica e Preço", "C) Maior Desconto", "D) Maior Preço para Venda"],
            "resposta": "D"
        },
        {
            "pergunta": "Qual fase vem imediatamente antes da fase de lances na licitação?",
            "opcoes": ["A) Edital", "B) Homologação", "C) Análise de Propostas", "D) Habilitação"],
            "resposta": "C"
        }
    ]

    print("--- ⚖️  BEM-VINDO AO SIMULADOR DE LICITAÇÕES ⚖️  ---")
    print("Responda corretamente para ganhar pontos e aprender sobre a Lei 14.133!\n")

    for i, q in enumerate(perguntas):
        print(f"Pergunta {i+1}: {q['pergunta']}")
        for opcao in q['opcoes']:
            print(opcao)
        
        resposta_usuario = input("Sua resposta (A/B/C/D): ").upper()
        
        if resposta_usuario == q['resposta']:
            print("✅ Correto! Você conhece as regras.\n")
            pontuacao += 10
        else:
            print(f"❌ Errado! A resposta correta era {q['resposta']}.\n")
        time.sleep(1)

    print(f"--- 🏁 FIM DE JOGO! 🏁 ---")
    print(f"Sua pontuação final: {pontuacao}/{len(perguntas)*10}")
    
    if pontuacao == len(perguntas)*10:
        print("Parabéns! Você é um verdadeiro Pregoeiro!")
    elif pontuacao >= 10:
        print("Bom trabalho! Continue estudando a Lei 14.133.")
    else:
        print("Precisa estudar mais sobre os editais!")

# Iniciar o jogo
jogar_licitacao()
