"""
CAMADA 3 – DECISÓRIA
Verifica regras, histórico e elegibilidade. A decisão é baseada SOMENTE em
regras explícitas (arquivo regras.py) e sempre devolve as justificativas,
para que o aluno entenda por que recebeu aquele resultado (interpretabilidade).

Escolhas éticas documentadas:
  * A decisão usa só 4 variáveis: renda familiar, nº de pessoas na casa,
    semestre e CR. Nenhum dado demográfico entra no cálculo.
  * Casos a menos de 5% de um limite NÃO são decididos pela máquina:
    vão para revisão humana (human-in-the-loop).
  * Aluno de baixa renda com CR baixo não é simplesmente negado: vai para a
    assistência social, porque o CR baixo pode ser consequência da própria
    vulnerabilidade (trabalhar enquanto estuda, por exemplo).
"""

from dataclasses import dataclass, field

from .regras import EDITAL, SALARIO_MINIMO_REFERENCIA
from .util import reais


def _n(valor: float, casas: int = 2) -> str:
    return f"{valor:.{casas}f}".replace(".", ",")

BOLSA_INTEGRAL = "Bolsa integral (100%)"
BOLSA_PARCIAL = "Bolsa parcial (50%)"
CREDITO = "Crédito estudantil"
NAO_ELEGIVEL = "Não elegível neste edital"
REVISAO_HUMANA = "Encaminhado para análise da assistência social"


@dataclass
class Decisao:
    resultado: str
    justificativas: list = field(default_factory=list)
    revisao_humana: bool = False
    variaveis_usadas: dict = field(default_factory=dict)
    renda_per_capita: float = 0.0


def _perto_do_limite(valor_sm: float) -> float | None:
    for limite in (EDITAL["limite_integral_sm"], EDITAL["limite_parcial_sm"]):
        if abs(valor_sm - limite) / limite <= EDITAL["margem_revisao"]:
            return limite
    return None


def decidir(renda_familiar: float, membros: int, semestre: int, cr: float | None) -> Decisao:
    usadas = {"renda_familiar": renda_familiar, "membros": membros,
              "semestre": semestre, "cr": cr}
    just = []

    if membros <= 0 or renda_familiar < 0 or semestre <= 0:
        return Decisao(REVISAO_HUMANA, ["Os dados informados estão inconsistentes."],
                       True, usadas)

    rpc = renda_familiar / membros
    em_sm = rpc / SALARIO_MINIMO_REFERENCIA
    just.append(f"Renda por pessoa: {reais(rpc)} ({_n(em_sm)} salários mínimos de referência).")

    calouro = semestre == 1
    if calouro:
        just.append("Você está no 1º semestre, então o CR não é exigido.")
        cr_ok_bolsa = cr_ok_credito = True
    else:
        cr = cr if cr is not None else 0.0
        cr_ok_bolsa = cr >= EDITAL["cr_minimo_bolsa"]
        cr_ok_credito = cr >= EDITAL["cr_minimo_credito"]
        just.append(f"Seu CR é {_n(cr, 1)} (mínimo para bolsa: {_n(EDITAL['cr_minimo_bolsa'], 1)}).")

    if em_sm <= EDITAL["limite_integral_sm"]:
        faixa = BOLSA_INTEGRAL
        just.append(f"A renda por pessoa está até {_n(EDITAL['limite_integral_sm'], 1)} SM: faixa da bolsa integral.")
    elif em_sm <= EDITAL["limite_parcial_sm"]:
        faixa = BOLSA_PARCIAL
        just.append(f"A renda por pessoa está entre {_n(EDITAL['limite_integral_sm'], 1)} e "
                    f"{_n(EDITAL['limite_parcial_sm'], 1)} SM: faixa da bolsa parcial.")
    else:
        faixa = None
        just.append(f"A renda por pessoa passa de {_n(EDITAL['limite_parcial_sm'], 1)} SM, "
                    "o limite das bolsas.")

    revisao = False
    if faixa and cr_ok_bolsa:
        resultado = faixa
    elif faixa and cr_ok_credito:
        resultado = CREDITO
        just.append("O CR está abaixo do mínimo para bolsa, mas atende ao crédito estudantil.")
    elif faixa:
        resultado = REVISAO_HUMANA
        revisao = True
        just.append("Você tem perfil de renda para bolsa, mas o CR está baixo. Em vez de negar, "
                    "a assistência social vai avaliar seu caso, porque o desempenho pode ter "
                    "sido afetado pela sua situação.")
    elif cr_ok_credito:
        resultado = CREDITO
        just.append("Você pode solicitar o crédito estudantil.")
    else:
        resultado = NAO_ELEGIVEL
        just.append("Renda acima do limite e CR abaixo do mínimo para crédito.")

    limite = _perto_do_limite(em_sm)
    if limite and not revisao:
        revisao = True
        just.append(f"Sua renda está muito perto do limite de {_n(limite, 1)} SM. Esse resultado é "
                    "PRELIMINAR: um analista humano vai conferir os documentos antes de confirmar.")

    return Decisao(resultado, just, revisao, usadas, rpc)
