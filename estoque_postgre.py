import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "GFUNCs"))

import funcoes_gerais as fg
import est_postgre_func as efun



def sistema_estoque():
    while True:
        options = input("== Bem-vindo ao sistema de estoque do Coffee Shops Tia Rosa. ==\n"
        "== Escolha um número: ==\n"
        "1. Atualizar quantidades em estoque;\n"
        "2. Verificar níveis de ingredientes em estoque;\n"
        "3. Listar ingredientes do estoque;\n"
        "4. Adicionar novo ingrediente;\n"
        "5. Encerrar aplicação.\n"
        "======================\n")

        if options == "1":
            efun.att()
        elif options == "2":
            efun.level()
        elif options == "3":
            efun.showIng()
        elif options == "4":
            efun.adicionar_ingrediente()
        elif options == "5":
            fg.end("Sistema de Estoque")
            break
        else:
            fg.invalid(options)

if __name__ == "__main__":
    sistema_estoque()