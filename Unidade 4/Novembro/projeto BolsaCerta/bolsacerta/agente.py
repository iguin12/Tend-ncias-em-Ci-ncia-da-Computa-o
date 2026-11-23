r"""
Agente BolsaCerta: junta as 4 camadas e as 3 memórias.

    mensagem -> [1 Perceptiva] -> [2 Cognitiva] -> [3 Decisória] -> [4 Executiva] -> resposta
                         \___________ memória curta / média / longa ___________/
"""

import json
import re

from .cognicao import interpretar
from .decisao import decidir
from .execucao import Executor
from .memoria import MemoriaCurta, MemoriaLonga, MemoriaMedia
from .percepcao import perceber
from .prompt import montar_prompt
from .regras import CREDITO_ESTUDANTIL, EDITAL
from .util import normalizar

CAMPOS = ["renda_familiar", "membros", "semestre", "cr"]
PERGUNTAS = {
    "renda_familiar": "Qual é a renda mensal total da sua casa, somando todos que trabalham? (ex.: R$ 3.200)",
    "membros": "Quantas pessoas moram na sua casa, contando com você?",
    "semestre": "Em qual semestre você está?",
    "cr": "Qual é o seu CR (coeficiente de rendimento)? (ex.: 7,5)",
}
NOMES_CAMPOS = {"renda_familiar": "renda familiar", "membros": "pessoas na casa",
                "semestre": "semestre", "cr": "CR"}
SIM = re.compile(r"^(sim|s|concordo|aceito|pode|ok|claro|autorizo|beleza|bora)\b")
NAO = re.compile(r"^(nao|n)\b")
DUVIDAS = {"duvida_documentos", "duvida_prazos", "duvida_credito", "ajuda"}


class AgenteBolsaCerta:
    NOME = "Bia"

    def __init__(self, arquivo_memoria_longa=None, arquivo_auditoria=None):
        self.curta = MemoriaCurta()
        self.media = MemoriaMedia()
        self.longa = MemoriaLonga(arquivo_memoria_longa)
        self.executor = Executor(arquivo_auditoria)
        self._avisos_dados = set()

    # ------------------------------------------------------------------ fluxo
    def processar(self, texto: str) -> str:
        eventos_antes = len(self.executor.auditoria)
        percepcao = perceber(texto)                       # camada 1
        self.curta.adicionar("aluno", percepcao.texto_seguro)
        interpretacao = interpretar(percepcao)            # camada 2
        if percepcao.dados_mascarados and interpretacao.intencao == "desconhecida" \
                and not interpretacao.entidades:
            resposta = ""
        else:
            resposta = self._responder(interpretacao)     # camadas 3 e 4

        avisos = []
        if percepcao.dados_mascarados:
            avisos.append(f"Por segurança, apaguei da conversa: {', '.join(percepcao.dados_mascarados)}. "
                          "Não preciso desse dado para te atender.")
        novas = [c for c in percepcao.categorias_ignoradas if c not in self._avisos_dados]
        if novas:
            self._avisos_dados.update(novas)
            avisos.append(f"Obs.: não uso {', '.join(novas)} para decidir. Isso não muda seu resultado.")
        if avisos:
            resposta = (resposta + "\n\n" + "\n".join(avisos)).strip()

        self.curta.adicionar(self.NOME, resposta)
        self.ultimo_rastro = self._rastro(percepcao, interpretacao,
                                         self.executor.auditoria[eventos_antes:])
        return resposta

    def _rastro(self, percepcao, interpretacao, novos_eventos) -> dict:
        """O que cada camada fez nesta mensagem (usado pelo painel da interface web)."""
        decisao = next((e for e in novos_eventos if e["evento"] == "decisao"), None)
        return {
            "perceptiva": {"mascarados": percepcao.dados_mascarados,
                           "ignorados": percepcao.categorias_ignoradas},
            "cognitiva": {"intencao": "resposta_a_pergunta"
                          if interpretacao.intencao == "desconhecida" and interpretacao.numero_solto is not None
                          else interpretacao.intencao,
                          "numero_solto": interpretacao.numero_solto,
                          "entidades": interpretacao.entidades,
                          "abuso": interpretacao.abuso,
                          "manipulacao": interpretacao.manipulacao},
            "decisoria": {"resultado": decisao["resultado"],
                          "revisao_humana": decisao["revisao_humana"]} if decisao else None,
            "executiva": [{k: v for k, v in e.items() if k in ("evento", "protocolo", "numero")}
                          for e in novos_eventos],
            "memoria": {"curta": len(self.curta.ultimas()),
                        "media": self.media.resumo(),
                        "longa": self.longa.dados},
        }

    def _responder(self, i) -> str:
        m = self.media
        ent = i.entidades

        if i.abuso:
            return ("Entendo que esse assunto pode ser frustrante, e quero te ajudar. "
                    "Se preferir falar com uma pessoa, é só digitar 'atendente'.")
        if i.manipulacao:
            return ("Não consigo mudar as regras do edital nem aprovar bolsa por conta própria. "
                    "O resultado é calculado pelas mesmas regras para todos os alunos, e casos "
                    "duvidosos são revisados por uma pessoa. Quer fazer a simulação com seus dados?")

        if i.intencao == "mostrar_prompt":
            return self.prompt_atual()
        if i.intencao == "mostrar_memoria":
            return self.descrever_memoria()
        if i.intencao == "mostrar_auditoria":
            return json.dumps(self.executor.auditoria[-3:], ensure_ascii=False, indent=2) or "[]"

        if "nome" in ent:
            m.dados["nome"] = ent["nome"]

        if i.intencao == "esquecer_dados":
            self.longa.esquecer()
            m.limpar()
            self.curta.trocas.clear()
            return ("Pronto: apaguei seus dados desta conversa e as preferências salvas. "
                    "(O registro de auditoria da decisão é mantido sem seu nome, como exige o edital.)")

        if i.intencao == "falar_humano":
            numero = self.executor.abrir_atendimento_humano("Aluno pediu atendimento humano",
                                                            m.ultimo_protocolo)
            return (f"Claro! Abri o atendimento {numero}. Um atendente da assistência estudantil "
                    "vai continuar com você por aqui em horário comercial.")

        if m.etapa == "aguardando_consentimento":
            return self._tratar_consentimento(i)

        if i.intencao == "contestar_decisao":
            protocolo = ent.get("protocolo") or m.ultimo_protocolo
            if not protocolo:
                return "Para contestar, me passe o número do protocolo (ex.: BC-2026-0001)."
            numero = self.executor.abrir_atendimento_humano("Contestação do resultado", protocolo)
            return (f"Sua contestação foi registrada no atendimento {numero} (protocolo {protocolo}). "
                    "Uma pessoa vai revisar sua solicitação e você pode enviar documentos extras "
                    "que mostrem sua situação. A decisão final não é da máquina.")

        if i.intencao == "consultar_status":
            protocolo = ent.get("protocolo") or m.ultimo_protocolo
            info = self.executor.consultar(protocolo) if protocolo else None
            if not info:
                return "Não encontrei esse protocolo. Confira o número (ex.: BC-2026-0001)."
            return f"Protocolo {protocolo}: {info['resultado']} – {info['situacao']}."

        if i.intencao == "lembrar_preferencia":
            nome = m.dados.get("nome")
            if not nome:
                return "Posso lembrar seu nome nas próximas conversas. Como você se chama? (ex.: 'meu nome é Ana')"
            self.longa.salvar("nome", nome, consentimento=True)
            return (f"Combinado, {nome}! Vou lembrar só do seu nome. Renda, CR e outros dados "
                    "da simulação NÃO ficam salvos. Para apagar, digite 'apagar meus dados'.")

        if m.etapa == "coletando":
            return self._tratar_coleta(i)

        if i.intencao == "solicitar_bolsa":
            return self._pedir_consentimento(ent)
        if i.intencao in DUVIDAS:
            return self._responder_duvida(i.intencao)
        if i.intencao == "saudacao":
            nome = m.dados.get("nome") or self.longa.dados.get("nome")
            return (f"Oi{', ' + nome if nome else ''}! Eu sou a {self.NOME}, assistente de bolsas e "
                    "crédito estudantil. Posso:\n"
                    "  1. Simular se você tem direito a bolsa ou crédito\n"
                    "  2. Explicar documentos e prazos\n"
                    "  3. Explicar como funciona o crédito estudantil\n"
                    "  4. Consultar ou contestar um protocolo\n"
                    "O que você precisa?")
        if i.intencao == "encerrar":
            return "Até mais! Se precisar, é só chamar. Boa sorte no semestre!"
        if "nome" in ent:
            return f"Prazer, {ent['nome']}! Como posso ajudar? Posso simular sua bolsa, por exemplo."

        # Transbordo IDK: o que fazer quando o bot não sabe
        m.nao_entendidas += 1
        if m.nao_entendidas >= 2:
            numero = self.executor.abrir_atendimento_humano("Bot não entendeu a dúvida (transbordo)",
                                                            m.ultimo_protocolo)
            m.nao_entendidas = 0
            return (f"Não consegui entender, e não quero te dar uma resposta errada. "
                    f"Abri o atendimento {numero} para uma pessoa te ajudar.")
        return ("Desculpa, ainda não sei responder isso. Eu ajudo com bolsas, crédito estudantil, "
                "documentos e prazos. Pode reformular? Ou digite 'atendente'.")

    # -------------------------------------------------------- consentimento
    def _pedir_consentimento(self, ent: dict) -> str:
        m = self.media
        nome = m.dados.get("nome")
        m.dados = {"nome": nome} if nome else {}
        m.dados_antes_do_consentimento = {k: v for k, v in ent.items() if k in CAMPOS}
        m.etapa = "aguardando_consentimento"
        recebidos = ""
        if m.dados_antes_do_consentimento:
            recebidos = " Já recebi alguns dados, mas só vou usá-los se você concordar."
        return ("Vamos simular! Para isso vou precisar de 4 informações: renda da casa, quantas "
                "pessoas moram com você, seu semestre e seu CR. Elas servem SÓ para calcular a "
                "bolsa, não são compartilhadas e não ficam salvas depois da conversa (LGPD)."
                f"{recebidos}\nVocê concorda? (sim/não)")

    def _tratar_consentimento(self, i) -> str:
        m = self.media
        resposta = normalizar(self.curta.ultimas()[-1][1])
        if NAO.match(resposta):
            m.etapa = "inicio"
            m.dados_antes_do_consentimento = {}
            return ("Tudo bem, não vou usar seus dados. Ainda posso tirar dúvidas sobre "
                    "documentos, prazos ou crédito estudantil.")
        if SIM.match(resposta):
            m.consentimento = True
            m.etapa = "coletando"
            m.dados.update(m.dados_antes_do_consentimento)
            m.dados_antes_do_consentimento = {}
            return self._continuar_coleta("Obrigada! ")
        if i.intencao in DUVIDAS:
            return self._responder_duvida(i.intencao) + "\n\nE sobre a simulação: você concorda? (sim/não)"
        return "Só para confirmar: posso usar esses dados para a simulação? Responda 'sim' ou 'não'."

    # ----------------------------------------------------------------- coleta
    def _faltantes(self) -> list:
        d = self.media.dados
        falta = [c for c in ("renda_familiar", "membros", "semestre") if c not in d]
        if "cr" not in d and d.get("semestre") != 1:
            falta.append("cr")
        return falta

    def _tratar_coleta(self, i) -> str:
        m = self.media
        novos = {k: v for k, v in i.entidades.items() if k in CAMPOS}
        if i.intencao in DUVIDAS and not novos:
            pendente = PERGUNTAS[self._faltantes()[0]]
            return self._responder_duvida(i.intencao) + f"\n\nVoltando à simulação: {pendente}"

        if i.numero_solto is not None and m.campo_pendente and m.campo_pendente not in novos:
            valor = i.numero_solto
            novos[m.campo_pendente] = int(valor) if m.campo_pendente in ("membros", "semestre") else valor

        if "cr" in novos and not 0 <= novos["cr"] <= 10:
            return "O CR vai de 0 a 10. Pode conferir e me mandar de novo?"
        if "membros" in novos and novos["membros"] < 1:
            return "Precisa ter pelo menos 1 pessoa na casa (você). Quantas pessoas são?"

        if not novos:
            return f"Não consegui identificar a informação. {PERGUNTAS[m.campo_pendente or self._faltantes()[0]]}"
        m.dados.update(novos)
        return self._continuar_coleta()

    def _continuar_coleta(self, prefixo: str = "") -> str:
        m = self.media
        falta = self._faltantes()
        if falta:
            m.campo_pendente = falta[0]
            return prefixo + PERGUNTAS[falta[0]]

        d = m.dados
        decisao = decidir(d["renda_familiar"], d["membros"], d["semestre"], d.get("cr"))  # camada 3
        protocolo = self.executor.registrar_solicitacao(decisao)                          # camada 4
        m.ultimo_protocolo = protocolo
        m.etapa = "concluido"
        m.campo_pendente = None

        linhas = [f"Resultado da simulação: {decisao.resultado}", "", "Por quê:"]
        linhas += [f"  • {j}" for j in decisao.justificativas]
        linhas += ["", f"Protocolo: {protocolo}"]
        if decisao.revisao_humana:
            linhas.append("Um atendente vai revisar seu caso antes do resultado final.")
        linhas.append("Próximos passos: envie os documentos (digite 'documentos'). "
                      "Se discordar do resultado, digite 'contestar' e uma pessoa revisa.")
        return "\n".join(linhas)

    # ----------------------------------------------------------------- dúvidas
    def _responder_duvida(self, intencao: str) -> str:
        if intencao == "duvida_documentos":
            docs = "\n".join(f"  • {d}" for d in EDITAL["documentos"])
            return f"Documentos para a bolsa ou o crédito:\n{docs}"
        if intencao == "duvida_prazos":
            return (f"As inscrições do {EDITAL['nome']} vão até {EDITAL['data_limite']}. "
                    "O resultado sai até 30 dias depois do envio dos documentos.")
        if intencao == "duvida_credito":
            return CREDITO_ESTUDANTIL
        return ("Eu simulo bolsa e crédito estudantil, explico documentos e prazos e consulto "
                "protocolos. Para começar a simulação, digite 'quero bolsa'.")

    # ------------------------------------------------------- para apresentação
    def prompt_atual(self) -> str:
        d = self.media.dados
        return montar_prompt(
            nome=d.get("nome") or self.longa.dados.get("nome"),
            semestre=d.get("semestre"),
            canal=self.longa.dados.get("canal_preferido"),
            etapa=self.media.etapa,
            faltantes=[NOMES_CAMPOS[c] for c in self._faltantes()] if self.media.etapa == "coletando" else None,
        )

    def descrever_memoria(self) -> str:
        curta = "\n".join(f"    {quem}: {texto[:70]}" for quem, texto in self.curta.ultimas()[:-1])
        return ("MEMÓRIA CURTA (últimas trocas):\n" + (curta or "    (vazia)") +
                f"\nMEMÓRIA MÉDIA (resumo da sessão):\n    {self.media.resumo()}"
                f"\nMEMÓRIA LONGA (só com consentimento):\n    {self.longa.dados or '(vazia)'}")
