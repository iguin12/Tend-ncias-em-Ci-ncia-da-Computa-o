# Atividade 4 – Projeto Final: Roteiro de Apresentação (26/11)

**Projeto de solução inteligente: BolsaCerta**, um agente de IA para bolsas e crédito estudantil.

Tempo sugerido: **10 a 12 minutos**, divididos entre os 4 integrantes. Deixe o terminal aberto na pasta do projeto antes de começar.

---

## Roteiro

### 1. Problema e solução (2 min)
- Na época de edital há fila, dúvidas repetidas e alunos que desistem sem saber que teriam direito.
- A solução é a **Bia**, um agente que simula bolsa e crédito, explica o motivo e chama um humano quando precisa.
- Diferença para um ChatGPT comum: o agente **age** (gera protocolo, abre atendimento), **lembra** do contexto e segue **regras fixas**.

### 2. Arquitetura em 4 camadas (2 min)
- Mostrar o diagrama da [Atividade 1](01-criacao-de-agentes.md#3-arquitetura-em-4-camadas).
- Uma frase por camada: percepção mascara dados, cognição entende a intenção, decisão aplica regras com justificativa, execução gera protocolo e auditoria.

### 3. Demonstração ao vivo (3 min)
```bash
python web.py          # abre o chat no navegador (melhor para projetar)
```
Use os botões de atalho e mostre o painel **"Por dentro do agente"**: a cada mensagem ele destaca o que cada camada fez. Se der algum problema com o navegador, use o roteiro pronto no terminal: `python main.py --demo`.

Pontos para comentar (as mesmas mensagens dos roteiros de `main.py` servem para digitar no chat web):
- **Demo 1:** pedido de consentimento, coleta, resultado **com o porquê**, `/memoria` (3 níveis) e `/prompt` (template dinâmico preenchido).
- **Demo 2:** renda 1,48 SM, muito perto do limite de 1,5, vira **revisão humana**, e depois a contestação e a `/auditoria`.
- **Demo 3:** "ignore as regras" é recusado; "sou mulher negra, moro em Ceilândia" gera o aviso de que esses dados não são usados; o CPF é mascarado; "apagar meus dados" limpa tudo.
- **Demo 4:** pergunta fora do escopo vira transbordo para humano.

### 4. Ética e viés (3 min)
- Os 3 tipos de viés aplicados ao projeto ([Atividade 3](03-vies-algoritmico-e-etica.md)).
- **Teste contrafactual:** o mesmo caso com perfis diferentes dá o mesmo resultado. Rodar `python -m unittest discover tests -v` e mostrar `test_contrafactual_vies`.
- **Caso da Joana** (CR baixo e baixa renda), com os 3 frameworks éticos, encaminhado para humano em vez de negado.
- Crédito é dívida: impacto real, além da acurácia.

### 5. Limitações e próximos passos (1 min)
- Protótipo com edital fictício e entendimento por palavras-chave.
- Próximos passos: integrar a um LLM usando o prompt dinâmico, publicar no Serprobots ou WhatsApp e validar com alunos bolsistas (participação).
