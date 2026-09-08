import funcoes_gerais
import funcoes_clientes

# A função responsável por executar o sistema de clientes no arquivo 'main.py' ou localmente:
def sistema_clientes():
    # Bloco de código que contem todas as funcionalidades do CRUD:
    while True:
        # A variável options permite navegar pelas funções do CRUD:
        options = input("Bem-vindo ao sistema de cadastro de clientes do Coffee Shops Tia Rosa\n"
        "Escolha um número de '1' a '6':\n"
        "1. Adicionar cliente;\n2. Procurar cliente;\n3. Alterar dados de cliente;\n"
        "4. Remover cliente;\n5. Mostrar lista de clientes;\n6. Fechar sistema.\n")
        
        if options == "1":
            funcoes_clientes.adicionar()
        elif options == "2":
            funcoes_clientes.procurar()
        elif options == "3":
            funcoes_clientes.alter()
        elif options == "4":
            funcoes_clientes.remover()
        elif options == "5":
            funcoes_clientes.printClentes()
        elif options == "6":
            funcoes_gerais.end("sistema de cadastro de clientes")
            break
        else:
            funcoes_gerais.invalid(options)

if __name__ == "__main__":
    sistema_clientes()