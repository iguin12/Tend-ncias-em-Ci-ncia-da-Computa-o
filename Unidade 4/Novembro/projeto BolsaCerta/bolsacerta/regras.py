"""
Regras do edital (FICTÍCIO) usadas pela camada decisória.

Todas as regras ficam neste arquivo, separadas do código do agente, para que
qualquer pessoa (inclusive quem não programa) consiga auditar o que o agente
considera na hora de decidir. Isso aplica o Princípio da Interpretabilidade.
"""

# Valor de referência configurável. Atualize para o salário mínimo vigente.
SALARIO_MINIMO_REFERENCIA = 1518.00

EDITAL = {
    "nome": "Edital fictício nº 01/2026 – Programa BolsaCerta",
    "data_limite": "15/12/2026",
    # Faixas de renda per capita, em salários mínimos (SM)
    "limite_integral_sm": 1.5,   # até 1,5 SM por pessoa -> bolsa integral (100%)
    "limite_parcial_sm": 3.0,    # até 3,0 SM por pessoa -> bolsa parcial (50%)
    # Desempenho acadêmico
    "cr_minimo_bolsa": 6.0,      # CR mínimo para manter bolsa (não vale para calouro)
    "cr_minimo_credito": 5.0,    # CR mínimo para crédito estudantil
    # Casos a menos de 5% de um limite vão para revisão humana
    "margem_revisao": 0.05,
    "documentos": [
        "RG e CPF do aluno",
        "Comprovante de residência atualizado",
        "Comprovante de renda de todos os moradores da casa (últimos 3 meses)",
        "Declaração de quantas pessoas moram na casa",
        "Histórico escolar ou comprovante de matrícula (calouros)",
    ],
}

CREDITO_ESTUDANTIL = (
    "O crédito estudantil é um financiamento da própria instituição: você paga "
    "parte da mensalidade durante o curso e o restante depois de formado, em "
    "parcelas, sem juros acima da inflação. Ele é indicado para quem tem renda "
    "acima do limite das bolsas ou não atinge o CR mínimo para bolsa."
)

# Dados que o agente NUNCA usa para decidir (mesmo que o aluno informe).
VARIAVEIS_PROIBIDAS_NA_DECISAO = [
    "gênero", "raça/cor", "idade", "região/bairro onde mora",
    "religião", "estado civil", "nome",
]
