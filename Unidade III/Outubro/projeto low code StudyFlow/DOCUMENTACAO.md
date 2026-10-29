# Documentação Técnica — StudyFlow

## 1. Apresentação

O **StudyFlow — Gerenciador Inteligente de Tarefas Acadêmicas** é uma aplicação web desenvolvida como atividade prática da disciplina de Tendências em Ciência da Computação, na Unidade III, utilizando a abordagem Low Code / No Code, com foco em Vibecode.

O sistema foi criado para auxiliar estudantes na organização e no gerenciamento de suas tarefas acadêmicas, permitindo cadastrar atividades, estabelecer prioridades, acompanhar prazos e visualizar o progresso dos estudos.

## 2. Integrantes do Projeto

- Dilson Ribeiro de Souza
- Igor Carvalho de Oliveira
- Lucas Fernandes Soares

## 3. Acesso à Aplicação

A aplicação está publicada e pode ser acessada diretamente pelo navegador:

**[Acessar o StudyFlow](https://studyflow-academico.lovable.app)**

## 4. Repositório do Código-Fonte

O código-fonte completo está disponível no repositório original do projeto:

**[GitHub — StudyFlow](https://github.com/Dilson217/StudyFlow)**

## 5. Objetivo do Sistema

Desenvolver uma ferramenta de gerenciamento de tarefas acadêmicas que permita ao estudante organizar suas atividades, acompanhar prazos e visualizar seu progresso.

A proposta é oferecer uma solução prática para o planejamento dos estudos, reunindo diferentes recursos em um único ambiente.

## 6. Tecnologias Utilizadas

As principais tecnologias e ferramentas utilizadas no desenvolvimento são:

- **React:** construção da interface da aplicação.
- **TypeScript:** tipagem e organização do código.
- **Vite:** ferramenta de desenvolvimento e build.
- **Tailwind CSS:** estilização e responsividade.
- **TanStack Router:** gerenciamento de rotas.
- **Zod:** validação de dados.
- **localStorage:** armazenamento local das tarefas.
- **Vitest:** execução de testes automatizados.
- **Testing Library:** testes dos componentes.
- **Playwright:** testes de interação no navegador.
- **Lovable:** plataforma utilizada como apoio ao desenvolvimento.
- **Git e GitHub:** controle de versão e gerenciamento do código-fonte.

## 7. Funcionalidades do Sistema

### 7.1 Cadastro de tarefas

Permite cadastrar atividades acadêmicas com as seguintes informações:

- Título;
- Descrição;
- Data de entrega;
- Prioridade;
- Status.

### 7.2 Edição e exclusão

O usuário pode atualizar as informações de uma tarefa cadastrada ou excluir atividades que não são mais necessárias.

### 7.3 Definição de prioridades

As tarefas podem ser classificadas em três níveis:

- Baixa;
- Média;
- Alta.

### 7.4 Gerenciamento de status

Cada tarefa pode apresentar um dos seguintes estados:

- Pendente;
- Em andamento;
- Concluída.

### 7.5 Pesquisa e filtros

O sistema permite pesquisar tarefas pelo título e filtrar as atividades conforme prioridade e situação.

### 7.6 Painel de acompanhamento

O painel apresenta indicadores para acompanhar a situação geral das atividades:

- Total de tarefas;
- Tarefas pendentes;
- Tarefas em andamento;
- Tarefas concluídas;
- Tarefas atrasadas;
- Prazos próximos;
- Progresso geral.

## 8. Regras de Negócio

O funcionamento do StudyFlow considera as seguintes regras:

1. O título da tarefa é obrigatório.
2. O título possui limite de 120 caracteres.
3. A descrição é opcional e possui limite de 1.000 caracteres.
4. A data de entrega é opcional.
5. A prioridade deve ser baixa, média ou alta.
6. O status deve ser pendente, em andamento ou concluído.
7. Tarefas concluídas não são consideradas nas indicações de atividades em aberto.
8. Tarefas atrasadas são identificadas conforme a data de entrega e o status.
9. Tarefas sem prazo definido continuam disponíveis na listagem.
10. Os dados são armazenados localmente no navegador.

## 9. Lógica e Algoritmos do Sistema

O StudyFlow utiliza regras automatizadas para organizar as tarefas e apresentar informações relevantes ao estudante.

Essa organização é realizada por meio de critérios previamente definidos no sistema, não dependendo de um modelo de inteligência artificial generativa.

### 9.1 Organização automática das tarefas

A organização das atividades considera critérios como:

1. Separação entre tarefas em aberto e concluídas.
2. Priorização dos prazos mais próximos.
3. Consideração do nível de prioridade da tarefa.
4. Utilização do status em andamento como critério adicional de desempate.

Dessa maneira, o estudante consegue visualizar as atividades que precisam de atenção primeiro.

### 9.2 Identificação de prazos

O sistema compara a data atual com a data de entrega das tarefas para identificar situações importantes:

- **Atrasadas:** tarefas em aberto cujo prazo já passou.
- **Para hoje:** tarefas com entrega na data atual.
- **Próximas do prazo:** tarefas com entrega nos próximos três dias.

### 9.3 Cálculo dos indicadores

Os indicadores do painel são atualizados com base nas tarefas cadastradas e em seus respectivos status e prazos.

Com essas informações, o sistema apresenta uma visão geral do andamento das atividades acadêmicas.

### 9.4 Persistência dos dados

O sistema utiliza o recurso `localStorage` do navegador para armazenar as tarefas.

Assim, as informações permanecem disponíveis após atualizar ou fechar e abrir novamente o navegador, desde que seja utilizado o mesmo navegador, perfil e endereço da aplicação.

## 10. Armazenamento e Limitações

Atualmente, o StudyFlow utiliza armazenamento local no navegador.

Isso significa que:

- Não possui sistema de autenticação de usuários.
- Não possui sincronização automática entre dispositivos.
- Não utiliza banco de dados remoto para armazenar as tarefas.
- Os dados dependem do armazenamento do navegador.
- Não possui backup remoto automático.

Por esse motivo, recomenda-se não cadastrar informações pessoais ou sensíveis.

## 11. Testes e Validação

Durante o desenvolvimento, foram realizados testes automatizados e testes de interação no navegador.

Conforme os resultados registrados durante a validação:

- 24 testes automatizados foram aprovados.
- Foram verificadas as operações de cadastro, edição e exclusão.
- Foram testados os filtros e indicadores.
- Foi verificada a persistência dos dados após atualização e reabertura do navegador.
- Foram avaliadas resoluções de dispositivos móveis.
- Não foram identificados erros de execução nos fluxos finais avaliados.

Os testes realizados não representam uma auditoria completa de segurança ou compatibilidade com todos os navegadores e dispositivos.

## 12. Desenvolvimento com Low Code / No Code e Vibecode

O StudyFlow foi desenvolvido com apoio da plataforma Lovable, explorando a abordagem de Vibecode.

Essa abordagem utiliza instruções em linguagem natural para auxiliar na criação de interfaces, implementação de funcionalidades e ajustes no código da aplicação.

Durante o desenvolvimento, foi necessário revisar as implementações, avaliar os resultados e realizar testes para verificar se as funcionalidades atendiam aos objetivos do projeto.

A ferramenta atuou como apoio ao processo de desenvolvimento, sendo importante o acompanhamento e a validação das funcionalidades implementadas.

## 13. Possibilidades de Evolução

Como melhorias futuras, o StudyFlow poderá receber:

- Sistema de cadastro e autenticação de usuários.
- Banco de dados remoto.
- Sincronização de tarefas entre dispositivos.
- Exportação e importação de atividades.
- Notificações de prazos.
- Relatórios de produtividade.
- Ampliação dos testes em diferentes navegadores e dispositivos.

## 14. Considerações Finais

O StudyFlow apresenta uma solução para o gerenciamento de tarefas acadêmicas, reunindo recursos de cadastro, edição, exclusão, organização por prioridades, acompanhamento de prazos e visualização do progresso.

O desenvolvimento permitiu aplicar conhecimentos relacionados à programação web, organização de código, validação de dados, testes de software e controle de versão.

Além disso, o projeto possibilitou explorar o uso de ferramentas de Vibecode como apoio ao desenvolvimento de software, demonstrando suas contribuições e limitações durante a construção de uma aplicação funcional.
