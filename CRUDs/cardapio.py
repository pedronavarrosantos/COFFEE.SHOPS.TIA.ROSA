import funcoes_gerais
import funcoes_cardapio

# A função responsável por executar o sistema do cardápio no arquivo 'main.py' ou localmente:
def sistema_cardapio():
    # Bloco de código que contem todas as funcionalidades do CRUD:
    while True:
        # A variável options permite navegar pelas funções do CRUD:
        options = input("Bem-vindo ao sistema de cardápio do Coffee Shops Tia Rosa\n"
        "Escolha um número de '1' a '6':\n"
        "1. Adicionar prato ao cardápio;\n2. Procurar prato no cardápio;\n3. Alterar dados de prato do cardápio;\n"
        "4. Remover prato do cardápio;\n5. Mostrar cardápio;\n6. Fechar sistema.\n")
        
        if options == "1":
            funcoes_cardapio.adicionar()
        elif options == "2":
            funcoes_cardapio.procurar()
        elif options == "3":
            funcoes_cardapio.alter()
        elif options == "4":
            funcoes_cardapio.remover()
        elif options == "5":
            funcoes_cardapio.show()
        elif options == "6":
            funcoes_gerais.end("Sistema de Cardápio")
            break
        else:
            funcoes_gerais.invalid(options)

if __name__ == "__main__":
    sistema_cardapio()