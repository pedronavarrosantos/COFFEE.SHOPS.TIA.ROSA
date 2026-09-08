import funcoes_gerais
import funcoes_pedidos

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
        "===============================================================\n")

        if options == "1":
            funcoes_pedidos.adicionar()
        elif options == "2":
            funcoes_pedidos.verificar()
        elif options == "3":
            funcoes_pedidos.modificar_pedido()
        elif options == "4":
            funcoes_pedidos.entrega()
        elif options == "5":
            funcoes_pedidos.cancelar()
        elif options == "6":
            funcoes_pedidos.fechar()
        elif options == "7":
            funcoes_gerais.end("Sistema de Cadastro de Pedidos")
            break
        else:
            funcoes_gerais.invalid(options)

if __name__ == "__main__":
    sistema_pedidos()