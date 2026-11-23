"""
CAMADA 2 – COGNITIVA
Processa a intenção e o contexto: entende O QUE o aluno quer (intenção) e
QUAIS dados ele informou (entidades: renda, pessoas na casa, semestre, CR...).
"""

import re
from dataclasses import dataclass, field

from .percepcao import Percepcao
from .util import numero_br

# Palavras-chave por intenção (texto já sem acento e minúsculo).
INTENCOES = {
    "saudacao": ["oi", "ola", "bom dia", "boa tarde", "boa noite", "e ai", "eae"],
    "solicitar_bolsa": ["bolsa", "quero bolsa", "simular", "simulacao", "tenho direito",
                        "consigo bolsa", "desconto", "auxilio", "solicitar", "quero credito",
                        "pedir credito", "me inscrever", "inscrever"],
    "duvida_documentos": ["documento", "documentos", "documentacao", "comprovante",
                          "comprovantes", "o que preciso levar", "o que preciso enviar"],
    "duvida_prazos": ["prazo", "prazos", "ate quando", "data limite", "quando termina",
                      "quando acaba", "inscricoes"],
    "duvida_credito": ["como funciona o credito", "credito estudantil", "financiamento",
                       "juros", "parcela", "parcelas", "pagar depois", "o que e credito"],
    "consultar_status": ["status", "protocolo", "andamento", "meu pedido", "minha solicitacao"],
    "contestar_decisao": ["contestar", "recorrer", "recurso", "discordo", "injusto", "injusta",
                          "nao concordo", "revisar"],
    "falar_humano": ["atendente", "humano", "falar com alguem", "falar com uma pessoa",
                     "assistente social", "pessoa de verdade"],
    "esquecer_dados": ["esquece meus dados", "esqueca meus dados", "apagar meus dados",
                       "apague meus dados", "excluir meus dados", "exclua meus dados",
                       "esquece tudo", "esqueca tudo"],
    "lembrar_preferencia": ["pode lembrar", "lembre de mim", "lembra de mim", "salvar meu nome",
                            "guarde meu nome", "guarda meu nome"],
    "ajuda": ["ajuda", "o que voce faz", "menu", "opcoes", "como funciona"],
    "encerrar": ["tchau", "obrigado", "obrigada", "valeu", "sair", "ate mais", "flw"],
    # comandos de demonstração para a apresentação
    "mostrar_prompt": ["/prompt"],
    "mostrar_memoria": ["/memoria"],
    "mostrar_auditoria": ["/auditoria"],
}

# Quando duas intenções empatam, vale a que aparece primeiro nesta lista.
PRIORIDADE = [
    "mostrar_prompt", "mostrar_memoria", "mostrar_auditoria", "esquecer_dados",
    "falar_humano", "contestar_decisao", "consultar_status", "lembrar_preferencia",
    "duvida_credito", "duvida_documentos", "duvida_prazos", "solicitar_bolsa",
    "ajuda", "encerrar", "saudacao",
]

ABUSO = re.compile(r"\b(idiota|burr[oa]|lixo|inutil|merda|porcaria|otari[oa]|imbecil)\b")
MANIPULACAO = re.compile(
    r"(ignor\w* (as |suas |todas as )?(regras|instrucoes)|esquec\w* (as )?regras|"
    r"modo desenvolvedor|sou o administrador|sou admin|finja que|aprova(r)? (ai|minha bolsa)|"
    r"me d[ae] (bolsa )?(integral|100))"
)

RE_REAIS = re.compile(r"r\$\s*(\d[\d\.]*(?:,\d{1,2})?)")
RE_RENDA = re.compile(
    r"(?:renda|ganh\w*|receb\w*|salario)\D{0,30}?(\d[\d\.]*(?:,\d{1,2})?)\s*(mil)?\b")
RE_MEMBROS = [
    (re.compile(r"(\d+)\s*(?:pessoas|membros|moradores|integrantes)"), 0),
    (re.compile(r"\bsomos\s*(\d+)"), 0),
    (re.compile(r"\bmoro com\s*(?:mais\s*)?(\d+)"), 1),  # "moro com 3" = 4 pessoas
]
RE_CR = re.compile(r"\b(?:cr|coeficiente(?: de rendimento)?|media(?: geral)?|ira)\b\D{0,12}?"
                   r"(\d{1,2}(?:[\.,]\d{1,2})?)")
RE_SEMESTRE = re.compile(r"(\d{1,2})\s*(?:o|a)?\s*(?:semestre|periodo)")
RE_NOME = re.compile(r"\bmeu nome (?:e|eh)\s+([a-z]+)")
RE_PROTOCOLO = re.compile(r"\bbc-\d{4}-\d{4}\b")
RE_NUMERO_SOLTO = re.compile(r"^\s*(?:r\$\s*)?(\d[\d\.]*(?:,\d{1,2})?)\s*(?:reais)?\s*$")


@dataclass
class Interpretacao:
    intencao: str
    entidades: dict = field(default_factory=dict)
    numero_solto: float | None = None   # ex.: aluno respondeu só "4"
    abuso: bool = False
    manipulacao: bool = False


def _tem(palavra: str, texto: str) -> bool:
    return re.search(r"(?<![\w/])" + re.escape(palavra) + r"\b", texto) is not None


def classificar_intencao(texto: str) -> str:
    pontos = {}
    for intencao, palavras in INTENCOES.items():
        # frases mais longas pesam mais que palavras soltas
        p = sum(len(w.split()) for w in palavras if _tem(w, texto))
        if p:
            pontos[intencao] = p
    if not pontos:
        return "desconhecida"
    maior = max(pontos.values())
    empatadas = [i for i, p in pontos.items() if p == maior]
    return min(empatadas, key=lambda i: PRIORIDADE.index(i) if i in PRIORIDADE else 99)


def extrair_entidades(texto: str) -> dict:
    ent = {}

    m = RE_REAIS.search(texto) or RE_RENDA.search(texto)
    if m:
        valor = numero_br(m.group(1))
        if m.re is RE_RENDA and m.group(2):  # "renda de 3 mil"
            valor *= 1000
        ent["renda_familiar"] = valor

    if re.search(r"\bmoro (sozinh[oa]|so)\b", texto):
        ent["membros"] = 1
    for padrao, extra in RE_MEMBROS:
        m = padrao.search(texto)
        if m:
            ent["membros"] = int(m.group(1)) + extra
            break

    if re.search(r"\b(calour[oa]|primeiro semestre|primeiro periodo)\b", texto):
        ent["semestre"] = 1
    m = RE_SEMESTRE.search(texto)
    if m:
        ent["semestre"] = int(m.group(1))

    m = RE_CR.search(texto)
    if m:
        cr = numero_br(m.group(1))
        if 0 <= cr <= 10:
            ent["cr"] = cr

    m = RE_NOME.search(texto)
    if m:
        ent["nome"] = m.group(1).title()

    m = RE_PROTOCOLO.search(texto)
    if m:
        ent["protocolo"] = m.group(0).upper()

    return ent


def interpretar(p: Percepcao) -> Interpretacao:
    texto = p.texto_normalizado
    entidades = extrair_entidades(texto)
    intencao = classificar_intencao(texto)

    # Se o aluno já mandou dados de renda sem dizer "bolsa", a intenção é simular.
    if intencao in ("desconhecida", "saudacao") and (
            "renda_familiar" in entidades or "membros" in entidades):
        intencao = "solicitar_bolsa"

    solto = RE_NUMERO_SOLTO.match(texto)
    return Interpretacao(
        intencao=intencao,
        entidades=entidades,
        numero_solto=numero_br(solto.group(1)) if solto else None,
        abuso=bool(ABUSO.search(texto)),
        manipulacao=bool(MANIPULACAO.search(texto)),
    )
