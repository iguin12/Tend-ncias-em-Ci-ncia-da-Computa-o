"""Funções auxiliares de texto e formatação."""

import re
import unicodedata


def normalizar(texto: str) -> str:
    """Deixa o texto minúsculo e sem acentos ("Média" -> "media")."""
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", texto.lower()).strip()


def numero_br(valor: str) -> float:
    """Converte números no formato brasileiro: '3.200,50' -> 3200.5; '7,5' -> 7.5."""
    valor = valor.strip()
    if "," in valor:
        return float(valor.replace(".", "").replace(",", "."))
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", valor):
        return float(valor.replace(".", ""))
    return float(valor)


def reais(valor: float) -> str:
    """Formata em reais: 1234.5 -> 'R$ 1.234,50'."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"
