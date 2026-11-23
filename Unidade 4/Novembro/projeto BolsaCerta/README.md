# Projeto Final A1 — BolsaCerta: Agente de IA para Bolsas e Crédito Estudantil

## Disciplina
Tendências em Ciência da Computação · Profa. Kadidja Valéria

## Unidade
Unidade 4 — Aplicações e Limitações (Agentes e Ética) — Novembro

## Integrantes

- Dilson Ribeiro de Souza
- Everton Wesley Pereira Oliveira
- Igor Carvalho de Oliveira
- Lucas Fernandes Soares

## 1. Apresentação

O **BolsaCerta** é um agente de IA que orienta estudantes sobre **bolsas de estudo e crédito estudantil**. A assistente virtual **Bia** conversa com o aluno, pede consentimento, coleta apenas os dados necessários, simula a elegibilidade de acordo com as regras de um edital (fictício), explica o motivo do resultado, gera protocolo e encaminha para um atendente humano quando o caso exige.

O projeto aplica os conteúdos da Unidade 4: arquitetura de agentes em 4 camadas, prompt dinâmico, gestão de memória, privacidade by design (LGPD), viés algorítmico e frameworks éticos.

## 2. Atividades da Unidade 4

| Data | Atividade | Entrega |
|---|---|---|
| 05/11 | Criação de agentes de IA | [01-criacao-de-agentes.md](atividades/01-criacao-de-agentes.md) + código em [`bolsacerta/`](bolsacerta) |
| 12/11 | Chatbot e especificação | [02-chatbot-especificacao-SPEC.md](atividades/02-chatbot-especificacao-SPEC.md) + [`main.py`](main.py) |
| 19/11 | Viés algorítmico e responsabilidade social | [03-vies-algoritmico-e-etica.md](atividades/03-vies-algoritmico-e-etica.md) + [testes de ética](tests/test_bolsacerta.py) |
| 26/11 | Projeto final (apresentação) | [04-projeto-final-apresentacao.md](atividades/04-projeto-final-apresentacao.md) |

## 3. Arquitetura

```
mensagem → [1 Perceptiva] → [2 Cognitiva] → [3 Decisória] → [4 Executiva] → resposta
               percepcao.py    cognicao.py     decisao.py      execucao.py
                    └──────── memória curta / média / longa (memoria.py) ────────┘
```

| Arquivo | Função |
|---|---|
| `bolsacerta/percepcao.py` | Camada perceptiva: recebe o texto, mascara CPF e e-mail e detecta dados que não podem ser usados |
| `bolsacerta/cognicao.py` | Camada cognitiva: intenções e entidades (renda, pessoas, semestre, CR) |
| `bolsacerta/decisao.py` | Camada decisória: regras com justificativa e revisão humana para casos no limite |
| `bolsacerta/execucao.py` | Camada executiva: protocolo, atendimento humano e auditoria |
| `bolsacerta/memoria.py` | Memória curta, média e longa (esta última só com consentimento) |
| `bolsacerta/prompt.py` | Template de prompt dinâmico com variáveis |
| `bolsacerta/regras.py` | Regras do edital fictício, separadas do código para facilitar a auditoria |
| `bolsacerta/agente.py` | Junta tudo: o agente Bia |
| `main.py` | Chatbot no terminal e roteiro de demonstração |
| `web.py` + `web/index.html` | Interface web do chat, com painel das 4 camadas e das memórias |
| `tests/` | 20 testes: funcionais, adversariais, de privacidade e de viés |

## 4. Como executar

Requer **Python 3.10+** e nenhuma biblioteca externa.

```bash
cd "Unidade 4/Novembro/projeto BolsaCerta"

python web.py                            # interface web do chat (abre no navegador)
python main.py --demo                     # roteiro pronto da apresentação (terminal)
python main.py                            # conversar com a Bia no terminal
python -m unittest discover tests -v      # rodar os testes
```

A interface web (`http://localhost:8000`) mostra o chat com a Bia e, ao lado, o painel **"Por dentro do agente"**, que exibe o que cada uma das 4 camadas fez em cada mensagem e o estado das 3 memórias. Para parar o servidor, use `Ctrl+C` no terminal.

Comandos extras durante a conversa: `/memoria`, `/prompt` e `/auditoria`.

## 5. Tecnologias

- **Linguagem:** Python 3 (somente a biblioteca padrão).
- **Abordagem:** agente baseado em regras explícitas, com camada de prompt dinâmico pronta para conectar a um LLM.
- **Especificação do chatbot:** fluxo e Canvas do guia *Desenvolvendo Chatbots* (Serprobots).

## 6. Principais decisões éticas

- A decisão usa **somente 4 variáveis**. Gênero, raça, idade, religião e região nunca entram no cálculo, e há um teste contrafactual que comprova isso.
- **Human-in-the-loop:** casos a menos de 5% de um limite e casos de baixa renda com CR baixo vão para revisão humana.
- **Interpretabilidade:** todo resultado vem com justificativa, e cada decisão fica registrada na auditoria.
- **LGPD:** consentimento antes da coleta, coleta mínima, CPF mascarado, memória longa restrita e direito de exclusão.
- **Remediação:** o aluno pode contestar qualquer resultado e falar com um humano.

## 7. Limitações

O edital, os valores e a instituição são **fictícios**, criados para fins acadêmicos. O protótipo simula a elegibilidade e não substitui a análise oficial de documentos.
