import clientes_postgre as clp
import estoque_postgre as ep
import pedidos_postgre as pp
import cardapio_postgre as cap
import funcoes_gerais as fg

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
            cap.sistema_cardapio()
        elif options == "2":
            clp.sistema_clientes()
        elif options == "3":
            ep.sistema_estoque()
        elif options == "4":
            pp.sistema_pedidos()
        elif options == "5":
            fg.end("sistema Cafeteria Tia Rosa")
            
            break
        else:
            fg.invalid(options)

if __name__ == "__main__":
    sistema_principal()