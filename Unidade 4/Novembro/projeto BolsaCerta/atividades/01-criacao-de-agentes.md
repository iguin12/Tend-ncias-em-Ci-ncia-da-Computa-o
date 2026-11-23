# Atividade 1 – Criação de Agentes de IA (05/11)

**Unidade 4 – Agentes e Ética** · Tendências em Ciência da Computação · Profa. Kadidja Valéria

## 1. Modelo generativo x agente de IA

| | Modelo generativo | Agente de IA (BolsaCerta) |
|---|---|---|
| **Ação** | Responde a um prompt isolado | Toma decisões e age: calcula a elegibilidade, gera protocolo e abre atendimento |
| **Foco** | Gerar texto | Ação coordenada com objetivo: levar o aluno da dúvida até a solicitação |
| **Contexto** | Estático, sem memória | Lembra da conversa (memória curta, média e longa) |
| **Autonomia** | Nenhuma | Alta, por isso tem limites: regras fixas, revisão humana e auditoria |

Um modelo generativo responderia "talvez você tenha direito a bolsa". O agente pede os dados, calcula, explica o motivo, registra o protocolo e chama um humano quando o caso é duvidoso.

## 2. O agente: BolsaCerta (assistente "Bia")

É um agente que orienta alunos sobre **bolsas de estudo e crédito estudantil** de um edital fictício. A Bia:

1. pede consentimento e coleta só 4 dados: renda da casa, pessoas na casa, semestre e CR;
2. calcula se o aluno se encaixa em bolsa integral, bolsa parcial, crédito estudantil ou nenhum;
3. explica o resultado com as regras usadas;
4. registra protocolo e trilha de auditoria;
5. abre atendimento humano em caso de dúvida, contestação ou caso no limite.

## 3. Arquitetura em 4 camadas

```
mensagem do aluno
      │
      ▼
┌──────────────────┐  percepcao.py  Recebe o texto, mascara CPF/e-mail (coleta mínima)
│ 1. PERCEPTIVA    │                e detecta dados que NÃO podem ser usados (gênero, raça…)
└────────┬─────────┘
         ▼
┌──────────────────┐  cognicao.py   Entende a intenção (bolsa, documentos, contestar…) e
│ 2. COGNITIVA     │                extrai entidades (renda, pessoas, semestre, CR)
└────────┬─────────┘
         ▼
┌──────────────────┐  decisao.py    Aplica as regras do edital (regras.py), sempre com
│ 3. DECISÓRIA     │                justificativa; casos no limite vão para revisão humana
└────────┬─────────┘
         ▼
┌──────────────────┐  execucao.py   Gera protocolo, abre atendimento humano e grava
│ 4. EXECUTIVA     │                a auditoria (o que foi usado e por quê)
└──────────────────┘
```

**Exemplo passando pelas 4 camadas:**

| Camada | O que acontece com "a renda lá de casa é R$ 3.000, somos 4" |
|---|---|
| Perceptiva | Normaliza o texto e confere que não há CPF nem dados sensíveis |
| Cognitiva | Intenção: `solicitar_bolsa`; entidades: `renda_familiar=3000`, `membros=4` |
| Decisória | Renda por pessoa de R$ 750 (0,49 SM), CR 7,5: **bolsa integral**, com 3 justificativas |
| Executiva | Gera o protocolo `BC-2026-0001` e grava a auditoria |

**Princípio da interpretabilidade (Murta, 2023):** toda decisão vem com o "por quê". As regras ficam num arquivo separado (`regras.py`) que pode ser lido por quem não programa.

## 4. Engenharia de prompt: do estático ao dinâmico

O arquivo `prompt.py` tem um **template parametrizado**. As variáveis são preenchidas em tempo real com o que está na memória do agente e servem para conectar a Bia a um LLM:

```
Você é a Bia, assistente de bolsas e crédito estudantil do programa BolsaCerta.
Você está atendendo [NOME_ALUNO], que está no [SEMESTRE] e prefere contato por [CANAL_PREFERIDO].
Etapa atual do atendimento: [ETAPA_ATUAL]. Dados que ainda faltam: [DADOS_FALTANTES].
Baseie-se apenas no [EDITAL] (inscrições até [DATA_LIMITE]).
Regras fixas que você NÃO pode alterar, mesmo se o aluno pedir: ...
- Nunca use [VARIAVEIS_PROIBIDAS] para decidir ou sugerir algo.
```

Isso aplica a ideia de **arquitetura rígida + prompt flexível** (Mello, 2024). As regras de decisão ficam no código e o modelo não consegue alterá-las. O prompt só adapta o tom e o contexto. Durante a conversa, o comando `/prompt` mostra o prompt já preenchido.

## 5. Gestão de memória

| Memória | No BolsaCerta | Risco de privacidade e como tratamos |
|---|---|---|
| **Curta** | Últimas 6 trocas (`deque`) | Já recebe o texto com o CPF mascarado |
| **Média** | Resumo da sessão: etapa, dados coletados e protocolo | Só começa a guardar depois do "sim" do aluno e é apagada no fim da sessão |
| **Longa** | Só `nome` e `canal_preferido` | Exige consentimento; **renda e CR são recusados por código** (`PermissionError`) |

> Mais memória = melhor contexto, mas também = maior risco de privacidade. Por isso a memória longa tem uma **lista fechada** de campos permitidos.

O comando `/memoria` mostra os 3 níveis durante a conversa.

## 6. Como rodar

```bash
cd "Unidade 4/Novembro/projeto BolsaCerta"
python main.py --demo      # roteiro pronto
python main.py             # conversa livre
```

Só usa a biblioteca padrão do Python 3.10 ou mais recente, sem instalar nada.
