import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "GFUNCs"))

import funcoes_gerais as fg
import clients_postgre_func as clpfun

# A função responsável por executar o sistema de clientes no arquivo 'main.py':
def sistema_clientes():
    # Bloco de código que contem todas as funcionalidades do CRUD:
    while True:
        # A variável options permite navegar pelas funções do CRUD:
        options = input("Bem-vindo ao sistema de cadastro de clientes do Coffee Shops Tia Rosa\n"
        "Escolha um número de '1' a '6':\n"
        "1. Adicionar cliente;\n2. Procurar cliente;\n3. Alterar dados de cliente;\n"
        "4. Remover cliente;\n5. Mostrar lista de clientes;\n6. Reativar cliente;\n7. Fechar sistema.\n")
        
        if options == "1":
            clpfun.adicionar()
        elif options == "2":
            clpfun.procurar()
        elif options == "3":
            clpfun.alter()
        elif options == "4":
            clpfun.remover()
        elif options == "5":
            clpfun.showClients()
        elif options == "6":
            clpfun.reativar()
        elif options == "7":
            fg.end("Sistema de Cadastro de Clientes")
            break
        else:
            fg.invalid(options)

if __name__ == "__main__":
    sistema_clientes()