"""
Gestão de memória em 3 níveis.

  * Curta  – só as últimas trocas da conversa (coerência imediata).
  * Média  – resumo da sessão atual: etapa e dados já coletados.
            É apagada quando a sessão termina.
  * Longa  – preferências duradouras, SÓ com consentimento explícito e SÓ
            de uma lista fechada de campos. Renda, CR e outros dados
            sensíveis nunca vão para a memória longa.

"Mais memória = melhor contexto, mas também = maior risco de privacidade."
"""

import json
from collections import deque
from pathlib import Path


class MemoriaCurta:
    def __init__(self, tamanho: int = 6):
        self.trocas = deque(maxlen=tamanho)

    def adicionar(self, quem: str, texto: str):
        self.trocas.append((quem, texto))

    def ultimas(self) -> list:
        return list(self.trocas)


class MemoriaMedia:
    def __init__(self):
        self.limpar()

    def limpar(self):
        self.etapa = "inicio"
        self.dados = {}
        self.campo_pendente = None
        self.ultimo_protocolo = None
        self.dados_antes_do_consentimento = {}
        self.consentimento = False
        self.nao_entendidas = 0

    def resumo(self) -> str:
        coletados = ", ".join(f"{k}={v}" for k, v in self.dados.items()) or "nenhum"
        return (f"etapa={self.etapa}; dados coletados: {coletados}; "
                f"consentimento={'sim' if self.consentimento else 'não'}; "
                f"último protocolo={self.ultimo_protocolo or '-'}")


class MemoriaLonga:
    CAMPOS_PERMITIDOS = {"nome", "canal_preferido"}

    def __init__(self, arquivo: str | None = None):
        self.arquivo = Path(arquivo) if arquivo else None
        self.dados = {}
        if self.arquivo and self.arquivo.exists():
            self.dados = json.loads(self.arquivo.read_text(encoding="utf-8"))

    def salvar(self, campo: str, valor: str, consentimento: bool):
        if not consentimento:
            raise PermissionError("Sem consentimento: nada é salvo na memória longa.")
        if campo not in self.CAMPOS_PERMITIDOS:
            raise PermissionError(f"O campo '{campo}' não pode ir para a memória longa.")
        self.dados[campo] = valor
        self._gravar()

    def esquecer(self):
        """Direito de exclusão da LGPD (art. 18)."""
        self.dados = {}
        if self.arquivo and self.arquivo.exists():
            self.arquivo.unlink()

    def _gravar(self):
        if self.arquivo:
            self.arquivo.write_text(json.dumps(self.dados, ensure_ascii=False, indent=2),
                                    encoding="utf-8")
