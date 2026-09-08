import funcoes_gerais
import funcoes_estoque

# A função responsável por executar o sistema de estoque no arquivo 'main.py':
def sistema_estoque():
    # No bloco de código abaixo se encontra o sistema de controle de quantidade em estoques:
    while True:
        options = input("== Bem-vindo ao sistema de estoque do Coffee Shops Tia Rosa. ==\n"
        "== Escolha um número: ==\n"
        "1. Atualizar quantidades em estoque;\n"
        "2. Verificar níveis de ingredientes em estoque;\n"
        "3. Listar ingredientes do estoque;\n"
        "4. Encerrar aplicação.\n"
        "======================\n")

        if options == "1":
            funcoes_estoque.atualizarEstoque()
        elif options == "2":
            funcoes_estoque.verificarNivel()
        elif options == "3":
            funcoes_estoque.lookIngredient()
        elif options == "4":
            funcoes_gerais.end("Sistema de Estoque")
            break
        else:
            funcoes_gerais.invalid(options)

if __name__ == "__main__":
    sistema_estoque()