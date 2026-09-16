# Programação Assistida e Automação com IA

## Identificação
- Nome: Igor Carvalho de Oliveira
- Ferramenta de IA utilizada: Claude (Anthropic)

## 1. Problema
Preciso automatizar o processamento das notas de uma turma de estudantes, calculando
automaticamente a média, a maior nota, a menor nota e a quantidade de estudantes aprovados
(considerando aprovação para nota igual ou superior a 6,0). Essa é uma tarefa repetitiva,
baseada em regras claras e sujeita a erros quando feita manualmente (ex.: em uma planilha),
o que a torna uma boa candidata à automação (Opção B do desafio).

## 2. Entrada
Uma lista de notas numéricas (valores decimais entre 0 e 10), representando as notas de
cada estudante de uma turma.

## 3. Processamento
O programa deve:
1. Validar se a lista de notas não está vazia e se todas as notas são numéricas e estão
   dentro do intervalo permitido (0 a 10);
2. Calcular a média aritmética da turma;
3. Identificar a maior e a menor nota;
4. Contar quantos estudantes têm nota igual ou superior a 6,0 (aprovados).

## 4. Saída esperada
- Média da turma;
- Maior nota;
- Menor nota;
- Quantidade de estudantes aprovados.

## 5. Prompt utilizado
```
Atue como desenvolvedor Python.

PROBLEMA:
Preciso analisar as notas de uma turma de estudantes.

ENTRADA:
Uma lista de notas (números decimais, entre 0 e 10).

SAÍDA ESPERADA:
Média da turma, maior nota, menor nota e quantidade de estudantes
aprovados (nota >= 6.0).

LINGUAGEM:
Python, utilizando apenas a biblioteca padrão.

RESTRIÇÕES:
- Não se preocupe ainda com validação de entrada nesta primeira versão;
- Mantenha o código simples e direto.

FORMATO:
1. Apresente o código;
2. Explique brevemente as principais linhas;
3. Mostre um exemplo de execução.
```

## 6. Código inicial
```python
"""
Processamento de Notas - Versão Inicial
Gerada com apoio de IA a partir do prompt estruturado (ver seção 5).
"""


def processar_notas(notas):
    media = sum(notas) / len(notas)
    maior = max(notas)
    menor = min(notas)
    aprovados = 0
    for nota in notas:
        if nota >= 6.0:
            aprovados += 1
    return media, maior, menor, aprovados


if __name__ == "__main__":
    notas = [7.5, 4.0, 9.0, 6.0, 3.5]
    media, maior, menor, aprovados = processar_notas(notas)

    print("Média:", media)
    print("Maior nota:", maior)
    print("Menor nota:", menor)
    print("Aprovados:", aprovados)
```

## 7. Análise crítica

Checklist da Etapa 3 aplicado à primeira versão:

- [x] Eu compreendo o código? Sim — é direto e usa apenas laços e funções nativas (`sum`, `max`, `min`).
- [x] O código atende ao problema definido? Parcialmente — funciona apenas no caso "feliz" (lista válida e não vazia).
- [x] Há bibliotecas que eu não conheço? Não, usa somente Python padrão.
- [x] Há operações que podem apagar ou sobrescrever dados? Não.
- [x] O código utiliza dados sensíveis? Não.
- [ ] Há tratamento de erros? **Não** — este é o principal problema encontrado.
- [x] Consigo explicar cada função ou bloco principal? Sim.
- [ ] Existem casos que o código não considera? **Sim**:
  - lista de notas vazia (gera `ZeroDivisionError` ao calcular a média);
  - notas fora do intervalo de 0 a 10 (aceitas sem alerta, distorcendo o resultado);
  - valores não numéricos na lista (gera `TypeError` sem mensagem clara para o usuário).

**Conclusão:** o código resolve corretamente o caso normal, mas não é seguro para uso real,
pois quebra ou produz resultados incorretos diante de entradas inesperadas.

## 8. Casos de teste

### Teste 1 — Caso normal
- Entrada: `[7.5, 4.0, 9.0, 6.0, 3.5]`
- Resultado esperado: média 6.0, maior 9.0, menor 3.5, 3 aprovados
- Resultado obtido (versão inicial): `Média: 6.0 / Maior: 9.0 / Menor: 3.5 / Aprovados: 3` ✅ **Passou**

### Teste 2 — Caso limite (lista vazia)
- Entrada: `[]`
- Resultado esperado: mensagem informando que não é possível processar uma lista vazia
- Resultado obtido (versão inicial): `ZeroDivisionError: division by zero` ❌ **Falhou** (o programa quebra em vez de tratar o erro)

### Teste 3 — Caso de erro (entrada inválida)
- Entrada: `[7.5, -3, 15, "oi"]` (nota negativa, nota acima de 10 e valor não numérico)
- Resultado esperado: mensagem informando qual nota é inválida e por quê
- Resultado obtido (versão inicial): `TypeError: unsupported operand type(s) for +: 'float' and 'str'` ❌ **Falhou** (erro genérico, sem indicar a causa ao usuário; além disso, `-3` e `15` seriam aceitos silenciosamente se não houvesse o valor "oi")

## 9. Problemas encontrados
1. Ausência total de tratamento de erros (lista vazia quebra o programa);
2. Ausência de validação do intervalo das notas (0 a 10);
3. Ausência de validação de tipo (valores não numéricos quebram o programa com erro pouco claro);
4. Média não arredondada, podendo gerar saídas com muitas casas decimais;
5. Falta de docstrings e type hints, dificultando a manutenção por outra pessoa.

## 10. Prompt de refatoração
```
Revise o código abaixo.
O programa já funciona para o caso normal, mas falha nos seguintes casos:
- lista de notas vazia;
- notas fora do intervalo de 0 a 10;
- valores não numéricos na lista.

Analise:
- clareza;
- organização;
- duplicação;
- nomes de variáveis e funções;
- tratamento de erros.

Sugira melhorias sem alterar o comportamento esperado no caso normal.
Adicione tratamento de erros para os três casos citados,
usando uma exceção específica e mensagens claras.
Inclua type hints e docstrings.
Explique cada alteração proposta.

[CÓDIGO]
```

## 11. Código refatorado
```python
"""
Processamento de Notas - Versão Refatorada
Refatorada com apoio de IA a partir do prompt de revisão (ver seção 10).
"""

from typing import List, Tuple


NOTA_MINIMA = 0.0
NOTA_MAXIMA = 10.0
NOTA_APROVACAO = 6.0


class NotasInvalidasError(Exception):
    """Lançada quando a lista de notas está vazia ou contém valores inválidos."""


def validar_notas(notas: List[float]) -> None:
    """Valida que a lista não está vazia e que todas as notas são numéricas
    e estão dentro do intervalo permitido (0 a 10).

    Levanta NotasInvalidasError em caso de problema.
    """
    if not notas:
        raise NotasInvalidasError("A lista de notas não pode estar vazia.")

    for nota in notas:
        if not isinstance(nota, (int, float)) or isinstance(nota, bool):
            raise NotasInvalidasError(f"Nota inválida (não numérica): {nota!r}")
        if not (NOTA_MINIMA <= nota <= NOTA_MAXIMA):
            raise NotasInvalidasError(
                f"Nota fora do intervalo permitido (0 a 10): {nota}"
            )


def processar_notas(notas: List[float]) -> Tuple[float, float, float, int]:
    """Processa uma lista de notas de estudantes.

    Args:
        notas: lista de notas numéricas (0 a 10).

    Returns:
        Uma tupla (media, maior, menor, aprovados).

    Raises:
        NotasInvalidasError: se a lista estiver vazia ou contiver notas inválidas.

    Exemplo:
        >>> processar_notas([7.5, 4.0, 9.0, 6.0, 3.5])
        (6.0, 9.0, 3.5, 3)
    """
    validar_notas(notas)

    media = round(sum(notas) / len(notas), 2)
    maior = max(notas)
    menor = min(notas)
    aprovados = sum(1 for nota in notas if nota >= NOTA_APROVACAO)

    return media, maior, menor, aprovados


def exibir_resultado(notas: List[float]) -> None:
    """Processa e exibe o resultado de forma amigável, tratando erros."""
    try:
        media, maior, menor, aprovados = processar_notas(notas)
        print(f"Média: {media}")
        print(f"Maior nota: {maior}")
        print(f"Menor nota: {menor}")
        print(f"Aprovados: {aprovados} de {len(notas)}")
    except NotasInvalidasError as erro:
        print(f"Erro: {erro}")


if __name__ == "__main__":
    notas = [7.5, 4.0, 9.0, 6.0, 3.5]
    exibir_resultado(notas)
```

**Testes repetidos na versão refatorada:**
- Teste 1 (caso normal): `Média: 6.0 / Maior: 9.0 / Menor: 3.5 / Aprovados: 3 de 5` ✅
- Teste 2 (lista vazia): `Erro: A lista de notas não pode estar vazia.` ✅ (agora tratado)
- Teste 3 (entrada inválida): `Erro: Nota fora do intervalo permitido (0 a 10): -3` ✅ (agora tratado)

## 12. Comparação

| Critério | Inicial | Refatorado |
|---|---:|---:|
| Funcionamento correto | 3 | 5 |
| Clareza | 3 | 5 |
| Organização | 3 | 4 |
| Legibilidade | 3 | 5 |
| Tratamento de erros | 1 | 5 |

## 13. Reflexão
- **Onde a IA mais ajudou?** Na geração rápida da primeira versão funcional e na sugestão
  de uma estrutura de validação (exceção customizada, docstrings e type hints) que eu
  provavelmente levaria mais tempo para organizar sozinho.
- **Onde a IA errou?** A primeira versão, gerada a partir de um prompt propositalmente
  simples, não incluiu nenhum tratamento de erro — o que mostra que a qualidade da resposta
  depende diretamente da qualidade e do detalhamento do prompt.
- **O que precisei modificar?** Precisei definir explicitamente as regras de negócio (nota
  entre 0 e 10, aprovação a partir de 6,0) e pedir, em um segundo prompt, o tratamento dos
  casos de erro identificados nos testes.
- **Consigo explicar o código?** Sim — todas as funções são pequenas, com responsabilidade
  única (validar, processar, exibir), o que facilita a explicação linha a linha.

## 14. Take Away
Programar com IA não significa deixar a IA programar por mim. Significa **usar a IA como
uma parceira que acelera a escrita do código, mas cabe a mim entender o problema, validar
cada sugestão, testar com casos reais (inclusive os que quebram o programa) e assumir a
responsabilidade final pelo que é entregue.**

### Cinco regras para uso responsável de IA na programação
1. Nunca copiar e executar código gerado por IA sem antes ler e entender cada linha.
2. Sempre testar com casos normais, casos limite (vazio/extremo) e casos de erro antes de considerar a solução pronta.
3. Nunca compartilhar senhas, chaves de API ou dados pessoais/confidenciais em prompts.
4. Usar prompts estruturados (papel, problema, entrada, saída, restrições) em vez de pedidos genéricos, pois isso melhora significativamente a qualidade da resposta.
5. Tratar toda sugestão da IA como um rascunho a ser validado — a responsabilidade técnica final é sempre do desenvolvedor humano.
