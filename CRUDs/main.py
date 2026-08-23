"""
O presente arquivo serve apenas como interface principal em que o usuário poderá acessar todos os outros sistemas do projeto navegando aqui dentro.
"""
# Abaixo está a importação de todos os outros sistemas do projeto:
import tia_rosa_cardapio
import clientes
import estoque
import pedidos
# Função 'invalid()' emite texto padrão em caso de invalidez de input:
def invalid(options):
    linhaIgual(f"== O comando '{options}' não é válido. ==")
    print(f"== O comando '{options}' não é válido. ==")
    linhaIgual(f"== O comando '{options}' não é válido. ==")
# Função linhaIgual() imprime uma string apenas de caracteres '=' do mesmo tamanho de outra string selecionada dentro do programa, 
# o parâmetro é a própria string selecionada:
def linhaIgual(x):
    print("=" * len(x))
# A função 'sistema_principal()' serve para rodar o programa navegando entre os sistemas:
def sistema_principal():
    # O while abaixo realiza a navegação entre sistemas:
    while True:
        options = input("== Bem-vindo ao sistema do Coffee Shops Tia Rosa! ==\n== O que deseja acessar? ==\n"
        "== Escolha um número: ==\n"
        " 1. Cardápio;\n"
        " 2. Clientes;\n"
        " 3. Estoque;\n"
        " 4. Pedidos;\n"
        " 5. Sair do sistema.\n")

        if options == "1":
            tia_rosa_cardapio.sistema_cardapio()
        elif options == "2":
            clientes.sistema_clientes()
        elif options == "3":
            estoque.sistema_estoque()
        elif options == "4":
            pedidos.sistema_pedidos()
        elif options == "5":
            print("=================================================")
            print("== Encerrando sistema de cadastro de clientes. ==")
            print("=================================================")
            break
        else:
            invalid(options)

sistema_principal()