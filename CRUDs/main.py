import clientes
import estoque
import pedidos
import cardapio
import funcoes_gerais

def sistema_principal():
    while True:
        options = input("== Bem-vindo ao sistema do Coffee Shops Tia Rosa! ==\n== O que deseja acessar? ==\n"
        "== Escolha um número: ==\n"
        " 1. Cardápio;\n"
        " 2. Clientes;\n"
        " 3. Estoque;\n"
        " 4. Pedidos;\n"
        " 5. Sair do sistema.\n")

        if options == "1":
            cardapio.sistema_cardapio()
        elif options == "2":
            clientes.sistema_clientes()
        elif options == "3":
            estoque.sistema_estoque()
        elif options == "4":
            pedidos.sistema_pedidos()
        elif options == "5":
            funcoes_gerais.end("sistema Cafeteria Tia Rosa")
            
            break
        else:
            funcoes_gerais.invalid(options)

if __name__ == "__main__":
    sistema_principal()