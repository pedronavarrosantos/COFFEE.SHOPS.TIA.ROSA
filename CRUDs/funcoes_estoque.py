"""
Esse documento concentra as funções de manupulação do arquivo CRUD estoque.py
"""
import funcoes_gerais
import dicionarios_dados

dicionarios_dados.carregarcardapio()
dicionarios_dados.carregarEstoque()

# Função que salva ou cria o documento 'estoque.txt' com os dados atuais da lista 'ingredientes':
def saveEstoque():
    with open("estoque.txt", "w") as doc:
        for item in dicionarios_dados.ingredientes:
            doc.write(
                f"{item['id']};"
                f"{item['ingrediente']};"
                f"{item['quantidade']}\n"
            )

# For fim, todo o processo de extração de dados de 'cardapiotr.txt' e impressão dos dados em 'estoque.txt' é salvo de uma vez com a chamada da função abaixo:
saveEstoque()

# Função que atualiza quantidades em estoque:
def atualizarEstoque():
    while True:
        escolha = input("Como deseja acessar o ingrediente?\nEscolha um número:\n1. Nome;\n2. Número de identificação.\n"
        "== Ou digite '0' para retornar ao menu principal. ==\n"
        "====================================================\n")
        if escolha == "1":
            ingNome = input("Digite o nome do ingrediente:\n")
            found = False

            for line in dicionarios_dados.ingredientes:
                if ingNome == line["ingrediente"]:
                    found = True

                    try:
                        amount = int(input("Digite a quantidade disponível do ingrediente:\n"))
                    except ValueError:
                        funcoes_gerais.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                        print("== Você digitou um valor inválido. Digite apenas números. ==")
                        funcoes_gerais.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                        continue
                    if amount < 0:
                        funcoes_gerais.positiveOnly()
                    else:
                        line.update({
                            "quantidade": amount
                        })
                        print(f"== Valor de {ingNome} atualizado para {amount}. ==")
                        saveEstoque()
            if not found:
                funcoes_gerais.linhaIgual("== Ingrediente não encontrado. ==")
                print("== Ingrediente não encontrado. ==")
                funcoes_gerais.linhaIgual("== Ingrediente não encontrado. ==")
        elif escolha == "2":
            try:
                ingId = int(input("Digite o número identificador do ingrediente:"))
            except ValueError:
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                print("== Você digitou um valor inválido. Digite apenas números. ==")
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                continue
            found = False

            for line in dicionarios_dados.ingredientes:
                if ingId == line["id"]:
                    print(f"== O ingrediente com número identificador {ingId} é o(a) {line['ingrediente']}. ==")
                    found = True

                    try:
                        amount = int(input("Digite a quantidade disponível do ingrediente:"))
                    except ValueError:
                        funcoes_gerais.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                        print("== Você digitou um valor inválido. Digite apenas números. ==")
                        funcoes_gerais.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                        continue
                    if amount < 0:
                        funcoes_gerais.positiveOnly()
                    else:
                        line.update({
                            "quantidade": amount
                        })
                        print(f"== Valor de {line["ingrediente"]} atualizado para {amount}. ==")
                        saveEstoque()
            if not found:
                funcoes_gerais.linhaIgual("== Ingrediente não encontrado. ==")
                print("== Ingrediente não encontrado. ==")
                funcoes_gerais.linhaIgual("== Ingrediente não encontrado. ==")
        elif escolha == "0":
            funcoes_gerais.back()
            break
        else:
            funcoes_gerais.invalid(escolha)

# Função que verifica níveis de ingredientes em estoque:
def verificarNivel():
    while True:
        escolha = input("Escolha uma opção:\n 1. Ver ingredientes em nível crítico;\n 2. Ver ingredientes em nível médio;\n"
        " 3. Ver ingredientes em quantidade segura;\n 4. Ver níveis de todos os ingredientes.\n"
        "== Ou digite '0' para retornar. ==\n"
        "==================================\n")
        if escolha == "1":
            for line in dicionarios_dados.ingredientes:
                if line["quantidade"] <= 10:
                    if line["quantidade"] == 0:
                        print(f"== O estoque de {line['ingrediente']} está zerado! ==\n== Dar urgência à reposição. ==")
                    else:
                        print(f"== O estoque de {line['ingrediente']} tem apenas {line['quantidade']} unidades! ==\n== Dar prioridade à reposição. ==")
        elif escolha == "2":
            for line in dicionarios_dados.ingredientes:
                if line["quantidade"] >= 11 and line["quantidade"] <= 50:
                    print(f"== O estoque de {line['ingrediente']} tem {line['quantidade']} unidades. ==\n== Reposição necessária em breve. ==")
        elif escolha == "3":
            for line in dicionarios_dados.ingredientes:
                if line["quantidade"] > 50:
                    print(f"== O estoque de {line['ingrediente']} tem {line['quantidade']} unidades. ==")
        elif escolha == "4":
            for line in dicionarios_dados.ingredientes:
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
                funcoes_gerais.back()
                break
        else:
            funcoes_gerais.invalid(escolha)

# Função que imprime todos os ingredientes com suas quantidades:
def lookIngredient():
    for line in dicionarios_dados.ingredientes:
        print(f"{line['id']}. {line['ingrediente']}; Quantidade: {line['quantidade']}.")