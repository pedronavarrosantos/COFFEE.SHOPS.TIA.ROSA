"""
Esse documento concentra as funções de manupulação do arquivo CRUD tia_rosa_carcapio.py
"""

import funcoes_gerais

# Lista que guarda os pratos do cardápio em memória:
cardapio = []

# Função que carrega os pratos salvos no arquivo .txt para a lista 'cardapio':
def carregarcardapio():
    try:
        with open("cardapiotr.txt", "r") as doc:
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
    except FileNotFoundError:
        with open("cardapiotr.txt", "w") as doc:
            pass

carregarcardapio()

# Função que salva ou cria o documento caso ele ainda não exista:
def savedoc():
    with open("cardapiotr.txt", "w") as doc:
        for prato in cardapio:
            doc.write(
                f"{prato['identificação']};"
                f"{prato['nome']};"
                f"{prato['preço']};"
                f"{prato['ingredientes']};"
                f"{prato['descrição']}\n"
            )

# Função que adiciona pratos ao cardápio:
def adicionar():
    while True:
        rId = int(input("===================================================================\n"
        "== Digite o número de identificação do prato ou 0 para retornar: ==\n"
        "===================================================================\n"))

        if rId < 0:
            funcoes_gerais.positiveOnly()
            continue
        if rId != 0:
            for prato in cardapio:
                if rId == int(prato["identificação"]):
                    funcoes_gerais.linhaIgual("===Já existe um prato com essa identificação.===")
                    print("===Já existe um prato com essa identificação.===")
                    funcoes_gerais.linhaIgual("===Já existe um prato com essa identificação.===")
                    break
            else:
                rNome = input("== Digite o nome do prato: ==\n")
                rPreco = float(input("== Digite o preço do prato: ==\n"))

                if rPreco < 0:
                    funcoes_gerais.positiveOnly()
                    continue
                ingredientes = input("== Digite os ingredientes: ==\n")
                rIngredientes = "'" + ingredientes + "'"
                descricao = input("== Digite a descrição do prato: ==\n")
                rDescricao = "'" + descricao + "'"

                cardapio.append({
                    "identificação": rId,
                    "nome": rNome,
                    "preço": rPreco,
                    "ingredientes": rIngredientes,
                    "descrição": rDescricao
                })
                funcoes_gerais.linhaIgual(f"== Prato com número identificador '{rId}' e nome '{rNome}' adicionado ao cardápio. ==")
                print(f"== Prato com número identificador '{rId}' e nome '{rNome}' adicionado ao cardápio. ==")
                funcoes_gerais.linhaIgual(f"== Prato com número identificador '{rId}' e nome '{rNome}' adicionado ao cardápio. ==")
                savedoc()
        else:
            funcoes_gerais.back()
            break

# Função que procura pratos ao cardápio:
def procurar():
    while True:
        escolha = input("Como deseja procurar o prato?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação.\n Ou digite '0' para retornar.\n")
        found = False

        if escolha == "1":
            nome_prato = input("Digite o nome do prato:\n")

            for prato in cardapio:
                if nome_prato == prato["nome"]:
                    print(f"== Identificação: {prato['identificação']}; ==\n== Nome: {prato['nome']}; ==\n== Preço: {prato['preço']}; =="
                    f"\n== Ingredientes: {prato['ingredientes']}; ==\n== Descrição: {prato['descrição']}. ==")
                    print("======================")

                    found = True
                    break
            if not found:
                funcoes_gerais.linhaIgual("== Prato não encontrado. ==")
                print("== Prato não encontrado. ==")
                funcoes_gerais.linhaIgual("== Prato não encontrado. ==")
        elif escolha == "2":
            id_prato = int(input("Digite o número de indentificação do prato:\n"))
            for prato in cardapio:
                if id_prato == prato["identificação"]:
                    print(f"== Identificação: {prato['identificação']}; ==\n== Nome: {prato['nome']}; ==\n== Preço: {prato['preço']}; =="
                    f"\n== Ingredientes: {prato['ingredientes']}; ==\n== Descrição: {prato['descrição']}. ==")
                    print("======================")

                    found = True
                    break
            if not found:
                funcoes_gerais.linhaIgual("== Prato não encontrado. ==")
                print("== Prato não encontrado. ==")
                funcoes_gerais.linhaIgual("== Prato não encontrado. ==")
        elif escolha == "0":
            funcoes_gerais.back()
            break
        else:
            funcoes_gerais.invalid(escolha)

# Função 'att()' funciona em conjunto com a função subsequente 'alter()';
# 'att()' serve para o usuário escolher qual chave de algum prato do cardapio deseja atualizar;
# Recebe como parâmetros as variáveis 'key' (presente em 'alter()') e 'prato'.
def att(key, prato):
    while True:
        if  key == "1":
            print(f"== No momento a key 'número de identificação' tem valor {prato['identificação']} ==")
            newKey = int(input("== Digite o novo valor da key 'identificação'. ==\n"))
            
            if newKey < 0:
                funcoes_gerais.positiveOnly()
                continue
            found = False

            # O 'for'abaixo existe para evitar que, durante uma reatribuição da chave 'identificação', pratos fiquem com números identificadores repetidos.
            # O 'for' precisa ter uma variável diferente de 'prato', uma vez que a função já recebe um valor para essa variável, 
            # para isso, utiliza-se 'outro_prato":
            for outro_prato in cardapio:
                if outro_prato != prato:
                    if newKey == outro_prato["identificação"]:
                        found = True
                        funcoes_gerais.linhaIgual("== Outro prato já possui o número de identificação que você está tentando usar. ==")
                        print("== Outro prato já possui o número de identificação que você está tentando usar. ==")
                        funcoes_gerais.linhaIgual("== Outro prato já possui o número de identificação que você está tentando usar. ==")
                        continue
            if not found:
                prato.update({
                    "identificação": newKey
                })
                savedoc()
                print(prato)
                funcoes_gerais.changedKey()
                break
        elif  key == "2":
            print(f"== No momento a key 'nome' tem valor {prato['nome']} ==")
            newKey = input("== Digite o novo valor da key 'nome'. ==\n")
            prato.update({
                "nome": newKey
            })
            savedoc()
            print(prato)
            funcoes_gerais.changedKey()
            break
        elif  key == "3":
            print(f"== No momento a key 'preço' tem valor {prato['preço']} ==")
            newKey = float(input("== Digite o novo valor da key 'preço'. ==\n"))

            if newKey < 0:
                funcoes_gerais.positiveOnly()
                continue
            prato.update({
                "preço": newKey
            })
            savedoc()
            print(prato)
            funcoes_gerais.changedKey()
            break
        elif  key == "4":
            print(f"== No momento a key 'ingredientes' tem valor {prato['ingredientes']} ==")
            newKey = input("== Digite o novo valor da key 'ingredientes'. ==\n")
            prato.update({
                "ingredientes": newKey
            })
            savedoc()
            print(prato)
            funcoes_gerais.changedKey()
            break
        elif  key == "5":
            print(f"== No momento a key 'descrição' tem valor {prato['descrição']} ==")
            newKey = input("== Digite o novo valor da key 'descrição'. ==\n")
            prato.update({
                "descrição": newKey
            })
            savedoc()
            print(prato)
            funcoes_gerais.changedKey()
            break
            
        else:
            funcoes_gerais.invalid(key)
            break

# Função 'alter()' consegue manipular valores das chaves dos dicionários de cada prato e imprimir a alteração diretamente no documento do 'cardapiotr.txt':
def alter():
    while True:
        loc = input("== Para realizar alteração, localize o prato por seu nome ou número de identificação: ==\n"
        "Escolha um número:\n 1. Nome;\n 2. Número de identificação.\n"
            "Ou digite '0' para retornar.\n===========================\n")

        if loc == "1":
            nome_prato = input("===Digite o nome do prato:===\n")
            found = False

            for prato in cardapio:
                if nome_prato == prato["nome"]:
                    found = True
                    key = input("== Qual chave do prato deseja alterar? ==\n== Escolha um número: ==\n"
                    "1. Número identificador\n2. Nome\n3. Preço\n4. Ingredientes\n5. Descrição.\n=============\n"
                    "== Ou digite qualquer outro comando para retornar ==\n=============\n")
                    att(key, prato)
                    break
            if not found:
                print("=========================================================")
                print(f"== Prato com nome '{nome_prato}' não consta no cardápio. ==")
                print("=========================================================\n")
        elif loc == "2":
            while True:
                try:
                    id_prato = int(input("== Digite o número de identificação: ==\n"))
                    break
                except ValueError:
                    print("== Esse campo aceita apenas números inteiros. ==")
            found = False

            for prato in cardapio:
                if id_prato == prato["identificação"]:
                    found = True
                    key = input("== Qual chave do prato deseja alterar? ==\n== Escolha um número: ==\n"
                    "1. Número identificador\n2. Nome\n3. Preço\n4. Ingredientes\n5. Descrição.\n=============\n"
                    "== Ou digite qualquer outro comando para retornar ==\n=============\n")
                    att(key, prato)
                    break
            if not found:
                print("==================================================================")
                print(f"== Prato com número identificador '{id_prato}' não consta no cardápio. ==")
                print("==================================================================\n")
        elif loc == "0":
                funcoes_gerais.back()
                break
        else:
            funcoes_gerais.invalid(loc)

# Função que remove pratos ao cardápio:
def remover():
    while True:            
        escolha = input("Como deseja remover o prato?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação;\nOu digite '0' para retornar ao menu principal.\n")

        if escolha == "0":
            funcoes_gerais.back()
            break
        elif escolha == "1":
            nome_prato = input("== Digite o nome do prato: ==\n")
            found = False

            for prato in cardapio:
                if nome_prato == prato["nome"]:
                    found = True

                    cardapio.remove(prato)

                    print("===================================")
                    print(f"== Prato {nome_prato} removido. ==")
                    print("===================================\n")
                    savedoc()
                    break
            if not found:
                print("=================================================================")
                print(f"== Prato com nome '{nome_prato}' já não existia no cardápio. ==")
                print("=================================================================\n")
        elif escolha == "2":
            while True:
                try:
                    id_prato = int(input("== Digite o número de identificação do prato: ==\n"))
                    break
                except ValueError:
                    print("== Esse campo aceita apenas números inteiros. ==")
            found = False

            for prato in cardapio:
                if id_prato == prato["identificação"]:
                    found = True

                    cardapio.remove(prato)

                    print("==================================")
                    print(f"== Prato {id_prato} removido. ==")
                    print("==================================\n")
                    savedoc()
                    break
            if not found:
                print("==================================================================================")
                print(f"== Prato com número de identificação '{id_prato}' já não existia no cardápio. ==")
                print("==================================================================================\n")
        else:
            funcoes_gerais.invalid(escolha)

# A função 'show()' permite ao usuário imprimir os pratos do cardápio:
def show():
    for prato in cardapio:
                print(f"> Número identificador: {prato['identificação']};\n> Nome: {prato['nome']};\n> Preço: R$:{prato['preço']};\n"
                f"> Ingredientes: {prato['ingredientes']};\n> Descrição: {prato['descrição']}\n====================")
