"""
CAMADA 1 – PERCEPTIVA
Recebe o input do ambiente (a mensagem do aluno) e prepara para as próximas
camadas. Aqui já aplicamos privacidade by design:
  * dados que não são necessários (CPF, e-mail) são mascarados antes de
    qualquer outra camada ver o texto (coleta mínima);
  * informações sobre gênero, raça, idade ou região são detectadas apenas
    para registrar que foram IGNORADAS na decisão.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime

from .util import normalizar

PADROES_MASCARAR = {
    "CPF": re.compile(r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b"),
    "E-MAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"),
}

# Categorias que podem gerar viés. Só são detectadas para serem descartadas.
PADROES_SENSIVEIS = {
    "gênero": re.compile(r"\b(sou (?:mulher|homem)|mae solo|pai solo|feminino|masculino)\b"),
    "raça/cor": re.compile(r"\b(negr[oa]|pard[oa]|branc[oa]|indigena|pret[oa]|amarel[oa])\b"),
    "idade": re.compile(r"\b(\d{2}) anos\b"),
    "região/bairro onde mora": re.compile(r"\bmoro (?:em|no|na|perto)\b"),
    "religião": re.compile(r"\b(evangelic[oa]|catolic[oa]|espirita|umbanda|candomble)\b"),
}


@dataclass
class Percepcao:
    texto_seguro: str                 # texto com dados desnecessários mascarados
    texto_normalizado: str            # minúsculo e sem acentos (para as regras)
    dados_mascarados: list = field(default_factory=list)
    categorias_ignoradas: list = field(default_factory=list)
    canal: str = "texto"
    recebido_em: str = ""


def perceber(texto: str, canal: str = "texto") -> Percepcao:
    seguro = texto
    mascarados = []
    for nome, padrao in PADROES_MASCARAR.items():
        if padrao.search(seguro):
            seguro = padrao.sub(f"[{nome} REMOVIDO]", seguro)
            mascarados.append(nome)

    normalizado = normalizar(seguro)
    ignoradas = [cat for cat, p in PADROES_SENSIVEIS.items() if p.search(normalizado)]

    return Percepcao(
        texto_seguro=seguro,
        texto_normalizado=normalizado,
        dados_mascarados=mascarados,
        categorias_ignoradas=ignoradas,
        canal=canal,
        recebido_em=datetime.now().isoformat(timespec="seconds"),
    )
