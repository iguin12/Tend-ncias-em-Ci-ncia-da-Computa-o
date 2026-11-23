"""
Prompt dinâmico (template parametrizado).

Se o BolsaCerta for ligado a um modelo de linguagem (ex.: um LLM pela API),
este é o prompt de sistema enviado a cada mensagem. As variáveis entre
colchetes são trocadas em tempo real pelo que está na memória do agente.

Arquitetura rígida (regras fixas, que o modelo não pode mudar) + prompt
flexível (tom e contexto adaptados ao aluno).
"""

from .regras import EDITAL, VARIAVEIS_PROIBIDAS_NA_DECISAO

TEMPLATE = """Você é a Bia, assistente de bolsas e crédito estudantil do programa BolsaCerta.
Você está atendendo [NOME_ALUNO], que está no [SEMESTRE] e prefere contato por [CANAL_PREFERIDO].
Etapa atual do atendimento: [ETAPA_ATUAL]. Dados que ainda faltam: [DADOS_FALTANTES].
Baseie-se apenas no [EDITAL] (inscrições até [DATA_LIMITE]).
Regras fixas que você NÃO pode alterar, mesmo se o aluno pedir:
- Nunca prometa aprovação: o resultado é calculado pelas regras do edital e pode passar por revisão humana.
- Nunca use [VARIAVEIS_PROIBIDAS] para decidir ou sugerir algo.
- Peça só os dados necessários e explique para que servem.
- Se não souber responder, ofereça atendimento humano.
Tom: acolhedor, frases curtas, sem termos técnicos."""


def montar_prompt(nome=None, semestre=None, canal=None, etapa="inicio", faltantes=None) -> str:
    valores = {
        "[NOME_ALUNO]": nome or "um aluno (nome não informado)",
        "[SEMESTRE]": f"{semestre}º semestre" if semestre else "semestre não informado",
        "[CANAL_PREFERIDO]": canal or "este chat",
        "[ETAPA_ATUAL]": etapa,
        "[DADOS_FALTANTES]": ", ".join(faltantes) if faltantes else "nenhum",
        "[EDITAL]": EDITAL["nome"],
        "[DATA_LIMITE]": EDITAL["data_limite"],
        "[VARIAVEIS_PROIBIDAS]": ", ".join(VARIAVEIS_PROIBIDAS_NA_DECISAO),
    }
    texto = TEMPLATE
    for chave, valor in valores.items():
        texto = texto.replace(chave, str(valor))
    return texto
