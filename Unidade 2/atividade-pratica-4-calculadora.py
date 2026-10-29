"""
Calculadora Simples
--------------------
Atividade prática: Programação Assistida por IA - Nível Básico

Objetivo: construir a lógica central de uma calculadora, com funções
matemáticas básicas e tratamento de erros (ex.: divisão por zero,
entrada inválida).
"""

import math


# ---------------------------------------------------------------------------
# Operações matemáticas
# ---------------------------------------------------------------------------

def somar(a, b):
    return a + b


def subtrair(a, b):
    return a - b


def multiplicar(a, b):
    return a * b


def dividir(a, b):
    if b == 0:
        raise ZeroDivisionError("Não é possível dividir por zero.")
    return a / b


def potencia(a, b):
    return math.pow(a, b)


def raiz_quadrada(a):
    if a < 0:
        raise ValueError("Não é possível calcular raiz quadrada de número negativo.")
    return math.sqrt(a)


# Mapeia as opções do menu para as funções correspondentes
OPERACOES = {
    "1": ("Soma (a + b)", somar, 2),
    "2": ("Subtração (a - b)", subtrair, 2),
    "3": ("Multiplicação (a * b)", multiplicar, 2),
    "4": ("Divisão (a / b)", dividir, 2),
    "5": ("Potência (a ^ b)", potencia, 2),
    "6": ("Raiz quadrada (√a)", raiz_quadrada, 1),
}


# ---------------------------------------------------------------------------
# Entrada e saída (interface de linha de comando)
# ---------------------------------------------------------------------------

def ler_numero(mensagem):
    """Lê um número do usuário, repetindo até que a entrada seja válida."""
    while True:
        valor = input(mensagem).strip().replace(",", ".")
        try:
            return float(valor)
        except ValueError:
            print("  ⚠ Entrada inválida. Digite um número (ex: 3.14).")


def exibir_menu():
    print("\n===== CALCULADORA =====")
    for chave, (descricao, _, _) in OPERACOES.items():
        print(f"  {chave}. {descricao}")
    print("  0. Sair")
    print("========================")


def formatar_resultado(valor):
    # Mostra números inteiros sem casas decimais desnecessárias
    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))
    return str(round(valor, 6))


def executar_operacao(opcao):
    descricao, funcao, num_args = OPERACOES[opcao]
    try:
        if num_args == 2:
            a = ler_numero("Digite o primeiro número: ")
            b = ler_numero("Digite o segundo número: ")
            resultado = funcao(a, b)
        else:
            a = ler_numero("Digite o número: ")
            resultado = funcao(a)

        print(f"\n✅ Resultado: {formatar_resultado(resultado)}")

    except ZeroDivisionError as erro:
        print(f"\n❌ Erro: {erro}")
    except ValueError as erro:
        print(f"\n❌ Erro: {erro}")
    except OverflowError:
        print("\n❌ Erro: resultado excede o limite numérico suportado.")


def main():
    print("Bem-vindo à Calculadora Simples (Atividade Prática - Nível Básico)")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Encerrando a calculadora. Até logo!")
            break

        if opcao not in OPERACOES:
            print("⚠ Opção inválida. Tente novamente.")
            continue

        executar_operacao(opcao)


if __name__ == "__main__":
    main()
