"""
CAMADA 4 – EXECUTIVA
Realiza a ação no mundo: registra a solicitação, gera protocolo, abre
atendimento humano e grava a trilha de auditoria (accountability).

A auditoria guarda só o necessário para explicar a decisão: as variáveis
usadas, o resultado e as justificativas. Não guarda nome nem a conversa.
"""

import json
from datetime import datetime
from pathlib import Path

from .decisao import Decisao


class Executor:
    def __init__(self, arquivo_auditoria: str | None = None, ano: int | None = None):
        self.ano = ano or datetime.now().year
        self.arquivo = Path(arquivo_auditoria) if arquivo_auditoria else None
        self.solicitacoes = {}
        self.atendimentos = []
        self.auditoria = []
        self._seq = 0

    def _auditar(self, evento: dict):
        evento["data_hora"] = datetime.now().isoformat(timespec="seconds")
        self.auditoria.append(evento)
        if self.arquivo:
            with self.arquivo.open("a", encoding="utf-8") as f:
                f.write(json.dumps(evento, ensure_ascii=False) + "\n")

    def registrar_solicitacao(self, decisao: Decisao) -> str:
        self._seq += 1
        protocolo = f"BC-{self.ano}-{self._seq:04d}"
        situacao = "Aguardando revisão humana" if decisao.revisao_humana else "Pré-aprovado (falta enviar documentos)"
        self.solicitacoes[protocolo] = {"resultado": decisao.resultado, "situacao": situacao}
        self._auditar({
            "evento": "decisao",
            "protocolo": protocolo,
            "variaveis_usadas": decisao.variaveis_usadas,
            "resultado": decisao.resultado,
            "revisao_humana": decisao.revisao_humana,
            "justificativas": decisao.justificativas,
        })
        return protocolo

    def abrir_atendimento_humano(self, motivo: str, protocolo: str | None = None) -> str:
        numero = f"ATD-{len(self.atendimentos) + 1:04d}"
        self.atendimentos.append({"numero": numero, "motivo": motivo, "protocolo": protocolo})
        if protocolo in self.solicitacoes:
            self.solicitacoes[protocolo]["situacao"] = "Em análise por um atendente"
        self._auditar({"evento": "atendimento_humano", "numero": numero,
                       "motivo": motivo, "protocolo": protocolo})
        return numero

    def consultar(self, protocolo: str) -> dict | None:
        return self.solicitacoes.get(protocolo)
