import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "CRUDs"))

import funcoes_gerais as fg
import card_postgre_func as cfun

# A função responsável por executar o sistema do cardápio no arquivo 'main.py':
def sistema_cardapio():
    # Bloco de código que contem todas as funcionalidades do CRUD:
    while True:
        # A variável options permite navegar pelas funções do CRUD:
        options = input("Bem-vindo ao sistema de cardápio do Coffee Shops Tia Rosa\n"
        "Escolha um número de '1' a '6':\n"
        "1. Adicionar prato ao cardápio;\n2. Procurar prato no cardápio;\n3. Alterar dados de prato do cardápio;\n"
        "4. Remover prato do cardápio;\n5. Mostrar cardápio;\n6. Reinserir prato no cardápio;\n7. Fechar Sistema.\n")
        
        if options == "1":
            cfun.adicionar()
        elif options == "2":
            cfun.procurar()
        elif options == "3":
            cfun.alter()
        elif options == "4":
            cfun.remover()
        elif options == "5":
            cfun.mostrar()
        elif options == "6":
            cfun.reativar()
        elif options == "7":
            fg.end("Sistema de Cardápio")
            break
        else:
            invalid(options)

if __name__ == "__main__":
    sistema_cardapio()