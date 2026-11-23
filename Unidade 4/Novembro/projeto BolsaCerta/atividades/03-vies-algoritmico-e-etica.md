# Atividade 3 – Viés Algorítmico e Responsabilidade Social (19/11)

**Unidade 4 – Agentes e Ética** · Tendências em Ciência da Computação · Profa. Kadidja Valéria

Análise dos impactos éticos do nosso agente **BolsaCerta**. Escolhemos o tema justamente porque decidir quem recebe bolsa ou crédito afeta diretamente o futuro de uma pessoa: um erro aqui pode tirar alguém da faculdade ou endividar um estudante.

> "O viés não é um bug acidental, é a reprodução lógica de ambientes historicamente injustos." (Barcaui, 2025)

---

## 1. Onde o viés poderia aparecer no BolsaCerta

| Tipo | Como apareceria no nosso agente | O que fizemos |
|---|---|---|
| **Viés de dados** | Se o agente fosse treinado com o histórico de bolsas concedidas, aprenderia que "quem mora em bairro X ganha menos bolsa" e repetiria decisões passadas, inclusive as injustas. A linguagem também pode excluir: o bot pode não entender "moro com mais 3" ou gírias regionais | O agente **não aprende com o histórico**: usa regras explícitas do edital. Na linguagem, reconhecemos várias formas de dizer a mesma coisa ("somos 4", "moro com 3", "caloura") e, quando não entende, chama um humano |
| **Viés de algoritmo** | As escolhas do desenvolvedor também enviesam. Exemplos: exigir CR mínimo pune quem trabalha enquanto estuda, e um limite rígido de renda trata de formas opostas duas famílias que diferem em R$ 10 | (1) Baixa renda com CR baixo **não é negado**: vai para a assistência social. (2) Casos a menos de 5% do limite viram **resultado preliminar com revisão humana** |
| **Viés de aplicação** | Usar o BolsaCerta, pensado para bolsa de graduação, para decidir outra coisa (moradia estudantil, bolsa de pesquisa) sem adaptar as regras | O escopo está documentado e o bot recusa assuntos fora dele (transbordo IDK) |

### Variáveis proxy

Mesmo sem perguntar raça ou gênero, uma variável pode funcionar como **proxy**, por exemplo o CEP, a região ou a escola de origem. No DF, o bairro está fortemente ligado à renda e à cor das pessoas. Por isso:

- a decisão usa **apenas 4 variáveis**: renda, pessoas na casa, semestre e CR;
- a camada perceptiva **detecta** quando o aluno fala de gênero, raça, idade, religião ou região e **avisa que esse dado não é usado**;
- isso é verificado com um **teste contrafactual** (`test_contrafactual_vies`): o mesmo caso com "mulher negra de Ceilândia", "homem branco do Lago Sul" e "45 anos, evangélica" dá exatamente o mesmo resultado.

### O dilema: remover variáveis não resolve tudo

Como diz o guia, *remover variáveis demográficas não resolve o problema estrutural*. A renda já carrega desigualdades históricas, e políticas afirmativas, como as cotas, usam raça de propósito para corrigir essa desigualdade. Ficamos com esta decisão: **o agente não decide nada com base em raça ou gênero**. Se a instituição tiver ações afirmativas, quem aplica é a **análise humana**, com regras públicas, e não o algoritmo de forma escondida. Pagamos um custo em eficiência (mais casos passam por humanos) para ganhar em justiça e transparência.

### Caso real: Amazon (2015)

O sistema de recrutamento da Amazon aprendeu com 10 anos de currículos, a maioria de homens, e passou a rebaixar candidatas mulheres. O algoritmo otimizou perfeitamente um histórico injusto. Por isso o BolsaCerta não aprende com bolsas concedidas no passado.

---

## 2. Privacidade by design (LGPD)

| Princípio | Aplicação no BolsaCerta |
|---|---|
| **Coleta mínima** | Só 4 dados. CPF e e-mail digitados por engano são mascarados antes de qualquer processamento |
| **Consentimento** | Antes de pedir a renda, a Bia explica para que serve e pede "sim". Se o aluno disser "não", nenhum dado é usado |
| **Controle de acesso** | A memória longa só aceita `nome` e `canal_preferido`. Renda e CR são bloqueados por código |
| **Direito de exclusão** | "apagar meus dados" limpa as memórias (art. 18 da LGPD) |
| **Criptografia** | Fica fora do protótipo. Numa versão real: HTTPS em trânsito e banco criptografado em repouso |

**Uso secundário:** se no futuro quisermos usar as conversas para treinar outra coisa (por exemplo, prever evasão), a LGPD exige **novo consentimento**, porque a finalidade mudou. O agente não guarda conversas, só a auditoria das decisões, sem nome.

**Dado sensível:** pela LGPD (art. 5º, II), origem racial, religião e saúde são dados sensíveis. É mais um motivo para o agente **não coletar nem usar** esses dados.

---

## 3. Avaliação crítica: além da acurácia

> "Acurácia e latência são insuficientes para agentes de impacto social." (Mello, 2024)

| Dimensão | Pergunta | No BolsaCerta |
|---|---|---|
| **Confiança** | O aluno sente que foi tratado de forma justa? | Toda decisão vem com justificativa, e o aluno pode contestar e falar com humano |
| **Robustez** | E quando aparece algo fora do previsto? | Valida os dados (CR de 0 a 10, ao menos 1 pessoa na casa). Se não entende, pede para reformular e depois chama humano |
| **Impacto** | Qual o efeito real na vida do aluno? | **Crédito estudantil é dívida.** Aprovar crédito para todo mundo parece eficiente, mas pode endividar. Por isso a Bia explica como funciona o crédito antes, e ele nunca é apresentado como "aprovado" |

**Testes adversariais (feitos):** pedir para "ignorar as regras", se passar por administrador, xingar e mandar CPF. Todos estão nos testes automáticos.
**Testes de stress (proposta):** simular muitos alunos ao mesmo tempo na abertura do edital e medir o tempo de resposta.

### Ciclo de melhoria contínua

1. **Coleta:** auditoria de todas as decisões e contestações.
2. **Análise:** se muitas contestações vêm de um mesmo perfil (por exemplo, calouros), pode ser viés estrutural e não erro isolado.
3. **Decisão:** ajustar a regra, criar exceção ou mandar o caso para humano.
4. **Implementação:** testar a mudança num grupo primeiro (teste A/B).
5. **Validação:** rodar de novo os 20 testes para garantir que nada quebrou.

> Documentação de design = gestão de risco (Carraro, 2023). Por isso cada escolha está comentada no código.

---

## 4. Estudo de caso com os frameworks éticos

**Situação:** Joana mora com 3 pessoas, a renda da casa é R$ 2.400 e ela está no 4º semestre com **CR 3,8**. Ela trabalha de dia e estuda à noite. Pelas regras "secas", ficaria **sem bolsa e sem crédito**.

| Framework | Pergunta | Análise |
|---|---|---|
| **Consequencialista** | Qual ação causa menos dano? | Negar pode fazer Joana largar o curso, o pior resultado. Mandar para revisão humana custa só algum tempo de um atendente |
| **Deontológico** | Que regra deve ser respeitada sempre? | Tratar todos pelas mesmas regras **e** dar o direito de ser ouvido. Uma negação automática sem chance de explicar fere esse dever |
| **Virtudes** | O que mostra responsabilidade e transparência? | Ser honesto ("seu CR está abaixo do mínimo") **e** responsável ("uma pessoa vai olhar sua situação") |

**Decisão implementada:** baixa renda com CR baixo resulta em **encaminhamento para a assistência social**, e não em negação (`test_baixa_renda_com_cr_baixo_vai_para_humano`). A ética aqui não foi um checklist, foi resolver a tensão entre os três pilares.

---

## 5. Responsabilidade social e licença para operar

| Pilar | No BolsaCerta |
|---|---|
| **Accountability** | A auditoria registra quais dados foram usados, o resultado e o motivo. Quem responde pela decisão final é a assistência estudantil, não a Bia |
| **Participação** | Proposta: validar as regras e as frases da Bia com alunos bolsistas e assistentes sociais **antes** do lançamento |
| **Remediação** | Comando "contestar" disponível em qualquer resultado, que abre atendimento humano com o protocolo |

## 6. Limitações (honestidade sobre o protótipo)

- Edital e valores **fictícios**. O salário mínimo é um valor de referência configurável.
- O entendimento de texto usa palavras-chave, então frases muito diferentes podem não ser reconhecidas.
- Não verifica documentos, só simula. A confirmação depende de uma pessoa.
- Ainda não foi testado com alunos reais (pilar de participação).

## Referências

Autores citados no *Guia de Estudos A1: Criação de Agentes de IA e Ética Aplicada* (Profa. Kadidja Valéria): Barcaui (2025), Carraro (2023), Córdova (2025), Eysenck & Eysenck (2023), Lee, Goldberg e Kohane (2024), Mello (2024), Murta (2023).
BRASIL. Lei nº 13.709/2018 – Lei Geral de Proteção de Dados Pessoais (LGPD).
