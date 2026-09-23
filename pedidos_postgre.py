import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "GFUNCs"))

import funcoes_gerais as fg
import peds_postgre_func as pfun

# A função responsável por executar o sistema de pedidos no arquivo 'main.py':
def sistema_pedidos():
    #No while abaixo ocorre toda a manipulação de pedidos:
    while True:
        options = input("== Bem-vindo ao sistema de pedidos do Coffee Shops Tia Rosa! ==\n"
        "== Escolha um número: ==\n"
        " 1. Criar novo pedido;\n"
        " 2. Verificar situação de pedido;\n"
        " 3. Modificar pedido;\n"
        " 4. Entregar pedido;\n"
        " 5. Cancelar pedido;\n"
        " 6. Fechar pedido;\n"
        " 7. Sair do sistema.\n"
        "====================\n")

        if options == "1":
            pfun.adicionar()
        elif options == "2":
            pfun.verificar()
        elif options == "3":
            pfun.modificar_pedido()
        elif options == "4":
            pfun.entrega()
        elif options == "5":
            pfun.cancelar()
        elif options == "6":
            pfun.fechar()
        elif options == "7":
            fg.end("Sistema de Cadastro de Pedidos")
            break
        else:
            fg.invalid(options)

if __name__ == "__main__":
    sistema_pedidos()