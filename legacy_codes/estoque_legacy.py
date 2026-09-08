"""
Sistema de estoque do Coffee Shops Tia Rosa

-> Este documento tem como insumo o arquivo txt 'cardapiotr.txt' que é controlado por outro fragmento do sistema da cafeteria, o 'tia_rosa_cardapio'.
-> Apenas a chave "ingredientes" de 'cardapiotr.txt' é utilizada, para cada linha de 'cardapiotr.txt' o trecho referente à chave "ingredientes" é fragmentado
para que sejam identificados os ingredientes.
-> Esses fragmentos são adicionados em outra lista de dicionários chamada 'ingredientes = []', as chaves dos dicionários são:

1. 'ingrediente' (que recebe os fragmentos filtrados de 'cardapiotr.txt');
2. 'id' (serve para enumerar os inregientes) e
3. 'quantidade'.

-> Este documento também conta com sistema de atualização de quantidade de ingredientes em estoque.
"""

cardapio = []

with open('cardapiotr.txt', 'r') as doc:
    for line in doc:
        rId, rNome, rPreco, rIngredientes, rDescricao = line.split(";")
        rId = int(rId)
        rPreco = float(rPreco)
        rDescricao = rDescricao.strip()

        cardapio.append({
            "identificação": rId,
            "nome": rNome,
            "preço": rPreco,
            "ingredientes": rIngredientes,
            "descrição": rDescricao
        })


# Função que salva ou cria o documento 'estoque.txt' com os dados atuais da lista 'ingredientes':
def savedoc():
    with open("estoque.txt", "w") as doc:
        for item in ingredientes:
            doc.write(
                f"{item['id']};"
                f"{item['ingrediente']};"
                f"{item['quantidade']}\n"
            )
# Função 'invalid()' emite texto padrão em caso de invalidez de input, recebe como parâmetro a variável 'escolha', ou 'loc' ou 'options':
def invalid(escolha):
    print("=================================")
    print(f"== O comando '{escolha}' não é válido. ==")
    print("=================================")
# Função linhaIgual() imprime uma string apenas de caracteres '=' do mesmo tamanho de outra string selecionada dentro do programa, 
# o parâmetro é a própria string selecionada:
def linhaIgual(x):
    lin = len(x)
    print("=" * lin)
# Função 'positiveOnly()' emite texto padrão quando o usuário tenta atribuir valor negativo a uma chave que só aceita valores positivos:
def positiveOnly():
    print("===================================================")
    print("== Essa variável aceita apenas valores positivos ==")
    print("===================================================\n")
# Função 'back()' emite texto padrão para informar ao usuário que o programa está retornando ao menu principal:
def back():
    linhaIgual("== Retornando. ==")
    print("== Retornando. ==")
    linhaIgual("== Retornando. ==")
# Carrega as quantidades já salvas em 'estoque.txt' (se o arquivo já existir), num dicionário
# 'ingrediente' -> 'quantidade', para que possam ser reaproveitadas ao montar a lista 'ingredientes' abaixo.
# Assim, quantidades já atualizadas em uma sessão anterior não são perdidas ao reprocessar o cardápio.
quantidades_salvas = {}
try:
    with open("estoque.txt", "r") as doc:
        for line in doc:
            _id, _ingrediente, _quantidade = line.split(";")
            quantidades_salvas[_ingrediente] = int(_quantidade)
except FileNotFoundError:
    # Primeira execução: ainda não existe 'estoque.txt', então não há quantidades pra recuperar.
    pass
# A lista "ingredientes = []" recebe os dicionários de cada ingrediente dos pratos:
ingredientes = []
# Variável 'counter' serve para aumentar gradativamente a enumeração dos ingredientes. É o insumo da chave "id"
counter = 0

# O for abaixo inicia a separação da chave "ingredientes" em fragmentos:
for prato in cardapio:
    fragmentos = prato["ingredientes"].split(",")

    # Remove espaços em branco de todos os fragmentos:
    fragmentos = [frag.strip() for frag in fragmentos]

    # Remove as aspas simples apenas do primeiro e do último fragmento da linha:
    fragmentos[0] = fragmentos[0].strip("'")
    fragmentos[-1] = fragmentos[-1].strip("'")

    # Com os fragmentos tratados, o append à lista "ingredientes = []" é feito no for abaixo:
    for frag in fragmentos:
        if frag not in [item["ingrediente"] for item in ingredientes]:
            quantidade_atual = quantidades_salvas.get(frag, 0)

            ingredientes.append({
                "id": counter,
                "ingrediente": frag,
                "quantidade": quantidade_atual
            })
            counter += 1

# For fim, todo o processo de extração de dados de 'cardapiotr.txt' e impressão dos dados em 'estoque.txt' é salvo de uma vez com a chamada da função abaixo:
savedoc()

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
            while True:
                escolha = input("Como deseja acessar o ingrediente?\nEscolha um número:\n1. Nome;\n2. Número de identificação.\n"
                "== Ou digite '0' para retornar ao menu principal. ==\n"
                "====================================================\n")
                if escolha == "1":
                    ingNome = input("Digite o nome do ingrediente:\n")
                    found = False

                    for line in ingredientes:
                        if ingNome == line["ingrediente"]:
                            found = True

                            try:
                                amount = int(input("Digite a quantidade disponível do ingrediente:\n"))
                            except ValueError:
                                linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                                print("== Você digitou um valor inválido. Digite apenas números. ==")
                                linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                                continue
                            if amount < 0:
                                positiveOnly()
                            else:
                                line.update({
                                    "quantidade": amount
                                })
                                print(f"== Valor de {ingNome} atualizado para {amount}. ==")
                                savedoc()
                    if not found:
                        linhaIgual("== Ingrediente não encontrado. ==")
                        print("== Ingrediente não encontrado. ==")
                        linhaIgual("== Ingrediente não encontrado. ==")
                elif escolha == "2":
                    try:
                        ingId = int(input("Digite o número identificador do ingrediente:"))
                    except ValueError:
                                linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                                print("== Você digitou um valor inválido. Digite apenas números. ==")
                                linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                                continue
                    found = False

                    for line in ingredientes:
                        if ingId == line["id"]:
                            print(f"== O ingrediente com número identificador {ingId} é o(a) {line['ingrediente']}. ==")
                            found = True

                            try:
                                amount = int(input("Digite a quantidade disponível do ingrediente:"))
                            except ValueError:
                                linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                                print("== Você digitou um valor inválido. Digite apenas números. ==")
                                linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                                continue
                            if amount < 0:
                                positiveOnly()
                            else:
                                line.update({
                                    "quantidade": amount
                                })
                                print(f"== Valor de {line["ingrediente"]} atualizado para {amount}. ==")
                                savedoc()
                    if not found:
                        linhaIgual("== Ingrediente não encontrado. ==")
                        print("== Ingrediente não encontrado. ==")
                        linhaIgual("== Ingrediente não encontrado. ==")
                elif escolha == "0":
                    back()
                    break
                else:
                    invalid(escolha)
        elif options == "2":
            while True:
                escolha = input("Escolha uma opção:\n 1. Ver ingredientes em nível crítico;\n 2. Ver ingredientes em nível médio;\n"
                " 3. Ver ingredientes em quantidade segura;\n 4. Ver níveis de todos os ingredientes.\n"
                "== Ou digite '0' para retornar. ==\n"
                "==================================\n")
                if escolha == "1":
                    for line in ingredientes:
                        if line["quantidade"] <= 10:
                            if line["quantidade"] == 0:
                                print(f"== O estoque de {line['ingrediente']} está zerado! ==\n== Dar urgência à reposição. ==")
                            else:
                                print(f"== O estoque de {line['ingrediente']} tem apenas {line['quantidade']} unidades! ==\n== Dar prioridade à reposição. ==")
                elif escolha == "2":
                    for line in ingredientes:
                        if line["quantidade"] >= 11 and line["quantidade"] <= 50:
                            print(f"== O estoque de {line['ingrediente']} tem {line['quantidade']} unidades. ==\n== Reposição necessária em breve. ==")
                elif escolha == "3":
                    for line in ingredientes:
                        if line["quantidade"] > 50:
                            print(f"== O estoque de {line['ingrediente']} tem {line['quantidade']} unidades. ==")
                elif escolha == "4":
                    for line in ingredientes:
                        if line["quantidade"] <= 10:
                            if line["quantidade"] == 0:
                                print(f"== O estoque de {line['ingrediente']} está zerado! ==\n== Dar urgência à reposição. ==")
                            else:
                                print(f"== O estoque de {line['ingrediente']} tem apenas {line['quantidade']} unidades! ==\n== Dar prioridade à reposição. ==")
                        if line["quantidade"] >= 11 and line["quantidade"] <= 50:
                            print(f"== O estoque de {line['ingrediente']} tem {line['quantidade']} unidades. ==\n== Reposição necessária em breve. ==")
                        else:
                            print(f"== O estoque de {line['ingrediente']} tem {line['quantidade']} unidades. ==")
                elif escolha == "0":
                        back()
                        break
                else:
                    invalid(escolha)
        elif options == "3":
            for line in ingredientes:
                print(f"{line['id']}. {line['ingrediente']}; Quantidade: {line['quantidade']}.")
        elif options == "4":
            print("=====================================")
            print("== Encerrando sistema de estoque. ==")
            print("=====================================")
            break
        else:
            invalid(options)

if __name__ == "__main__":
    sistema_estoque()