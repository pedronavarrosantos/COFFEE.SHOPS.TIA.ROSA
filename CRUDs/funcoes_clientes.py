"""
Esse arquivo concentra as funções de manipulação do sistema CRUD de clientes (cliente.py).
"""

import funcoes_gerais

# Lista que guarda os clientes do cardápio em memória:
clientes = []

# Função que carrega os clientes salvos no arquivo .txt para a lista 'clientes':
def carregarclientes():
    try:
        with open("clientes.txt", "r") as doc:
            for line in doc:
                user, userID, nTel, e_mail, cpf, points = line.split(";")
                userID = int(userID)
                points = int(points)
                nTel = str(nTel)
                cpf = str(cpf)

                clientes.append({
                    "clienteNom": user,
                    "clienteID": userID,
                    "telefone": nTel,
                    "e-mail": e_mail,
                    "cpf": cpf,
                    "pontos": points # Ao criar um novo cliente, o valor da chave pontos sempre será 0.
                })
    except FileNotFoundError:
        with open("clientes.txt", "w") as doc:
            pass

carregarclientes()

# Função que salva ou cria o documento caso ele ainda não exista:
def saveclient():
    with open("clientes.txt", "w") as doc:
        for cliente in clientes:
            doc.write(
                f"{cliente['clienteNom']};"
                f"{cliente['clienteID']};"
                f"{cliente['telefone']};"
                f"{cliente['e-mail']};"
                f"{cliente['cpf']};"
                f"{cliente['pontos']}\n"
            )       

# Função que adiciona clientes ao cardápio:
def adicionar():
    while True:
        user = str(input("==================================================\n"
        "== Digite o nome do cliente ou 0 para retornar: ==\n"
        "==================================================\n"))

        
        if user != "0":
            userID = clientes[-1]['clienteID'] + 1

            nTel = input("=============================================\n"
            "== Digite o número de telefone do cliente: ==\n"
            "=============================================\n")

            if nTel.isdigit() == True and (len(nTel) == 9 or len(nTel) == 11):
                e_mail = input("=================================\n"
                "== Digite o e-mail do cliente: ==\n"
                "=================================\n")

                if "@" in e_mail and e_mail[0] != "@" and e_mail.endswith(".com") == True:
                    cpf = input("==============================\n"
                    "== Digite o CPF do cliente: ==\n"
                    "==============================\n")

                    if cpf.isdigit() == True and len(cpf) == 11:
                        points = 0
                    else:
                        funcoes_gerais.linhaIgual("== CPF inválido ==")
                        print("== CPF inválido ==")
                        funcoes_gerais.linhaIgual("== CPF inválido ==")
                        continue
                else:
                    funcoes_gerais.linhaIgual("== E-mail inválido== ")
                    print("== E-mail inválido== ")
                    funcoes_gerais.linhaIgual("== E-mail inválido== ")
                    continue
            else:
                funcoes_gerais.linhaIgual("== Número de telefone inválido ==")
                print("== Número de telefone inválido ==")
                funcoes_gerais.linhaIgual("== Número de telefone inválido ==")
                continue
                    

            clientes.append({
                "clienteNom": user,
                "clienteID": userID,
                "telefone": nTel,
                "e-mail": e_mail,
                "cpf": cpf,
                "pontos": points
            })
            funcoes_gerais.linhaIgual(f"== Cliente com número identificador '{userID}' e nome '{user}' adicionado. ==")
            print(f"== Cliente com número identificador '{userID}' e nome '{user}' adicionado. ==")
            funcoes_gerais.linhaIgual(f"== Cliente com número identificador '{userID}' e nome '{user}' adicionado. ==")
            saveclient()
        else:
            funcoes_gerais.back()
            break

# Função que procura clientes ao cardápio:
def procurar():
    while True:
        escolha = input("Como deseja procurar o cliente?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação.\n Ou digite '0' para retornar.\n")
        found = False

        if escolha == "1":
            nome_cliente = input("Digite o nome do cliente:\n")

            for cliente in clientes:
                if nome_cliente == cliente["clienteNom"]:
                    print(f"== Nome: {cliente['clienteNom']}; ==\n== Número identificador: {cliente['clienteID']}; ==\n== Telefone: {cliente['telefone']}; =="
                    f"\n== E-mail: {cliente['e-mail']}; ==\n== CPF: {cliente['cpf']}. ==\n== Pontos: {cliente['pontos']}. ==")
                    print("======================")

                    found = True
                    break
            if not found:
                print("===========================")
                print("== Cliente não encontrado. ==")
                print("===========================\n")
        elif escolha == "2":
            try:
                id_cliente = int(input("Digite o número de indentificação do cliente:\n"))
            except ValueError:
                funcoes_gerais.linhaIgual("== ID inválido. Digite apenas números. ==")
                print("== ID inválido. Digite apenas números. ==")
                funcoes_gerais.linhaIgual("== ID inválido. Digite apenas números. ==")
                continue

            for cliente in clientes:
                if id_cliente == cliente["clienteID"]:
                    print(f"== Nome: {cliente['clienteNom']}; ==\n== Número identificador: {cliente['clienteID']}; ==\n== Telefone: {cliente['telefone']}; =="
                    f"\n== E-mail: {cliente['e-mail']}; ==\n== CPF: {cliente['cpf']}. ==\n== Pontos: {cliente['pontos']}. ==")
                    print("======================")

                    found = True
                    break
            if not found:
                funcoes_gerais.linhaIgual("== Cliente não encontrado. ==")
                print("== Cliente não encontrado. ==")
                funcoes_gerais.linhaIgual("== Cliente não encontrado. ==")
        elif escolha == "0":
            funcoes_gerais.back()
            break
        else:
            funcoes_gerais.invalid(escolha)

# Recebe como parâmetros as variáveis 'key' (presente em 'alter()') e 'cliente'.
def att(key, cliente):
    while True:
        if  key == "2":
            print(f"== No momento a key 'número de identificação' tem valor {cliente['clienteID']} ==")
            try:
                newKey = int(input("== Digite o novo valor da key 'clienteID'. ==\n"))
            except ValueError:
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para a key. ==")
                print("== Você digitou um valor inválido para a key. ==")
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para a key. ==")
                continue
            else:
                if newKey < 0:
                    funcoes_gerais.positiveOnly()
                    continue
                found = False

                # O 'for'abaixo existe para evitar que, durante uma reatribuição da chave 'clienteID', clientes fiquem com números identificadores repetidos.
                # O 'for' precisa ter uma variável diferente de 'cliente', uma vez que a função já recebe um valor para essa variável, 
                # para isso, utiliza-se 'outro_cliente":
                for outro_cliente in clientes:
                    if outro_cliente != cliente:
                        if newKey == outro_cliente["clienteID"]:
                            found = True
                            print("==================================================================================")
                            print("== Outro cliente já possui o número de identificação que você está tentando usar. ==")
                            print("==================================================================================")
                            break
                if not found:
                    cliente.update({
                        "clienteID": newKey
                    })
                    saveclient()
                    print(cliente)
                    funcoes_gerais.changedKey()
                    break
        elif  key == "1":
            print(f"== No momento a key 'clienteNom' tem valor {cliente['clienteNom']} ==")
            newKey = input("== Digite o novo valor da key 'clienteNom'. ==\n")
            cliente.update({
                "clienteNom": newKey
            })
            saveclient()
            print(cliente)
            funcoes_gerais.changedKey()
            break
        elif  key == "3":
            print(f"== No momento a key 'telefone' tem valor {cliente['telefone']} ==")
            newKey = input("== Digite o novo valor da key 'telefone'. ==\n")

            if newKey.isdigit() == True and len(newKey) <= 11 and len(newKey) >= 9:
                cliente.update({
                    "telefone": newKey
                })
                saveclient()
                print(cliente)
                funcoes_gerais.changedKey()
                break
            else:
                    funcoes_gerais.linhaIgual("== Número de telefone inválido ==")
                    print("== Número de telefone inválido ==")
                    funcoes_gerais.linhaIgual("== Número de telefone inválido ==")
                    continue
        elif  key == "4":
            print(f"== No momento a key 'e-mail' tem valor {cliente['e-mail']} ==")
            newKey = input("== Digite o novo valor da key 'e-mail'. ==\n")

            if "@" in newKey and newKey[0] != "@" and newKey.endswith(".com") == True:
                found = False

                for outro_cliente in clientes:
                    if outro_cliente is not cliente:
                        if newKey == cliente['e-mail']:
                            found = True

                            funcoes_gerais.linhaIgual("== Este e-mail já está em uso. ==")
                            print("== Este e-mail já está em uso. ==")
                            funcoes_gerais.linhaIgual("== Este e-mail já está em uso. ==")
                            break
                if not found:
                    cliente.update({
                        "e-mail": newKey
                    })
                    saveclient()
                    print(cliente)
                    funcoes_gerais.changedKey()
                    break
            else:
                    funcoes_gerais.linhaIgual("== E-mail inválido ==")
                    print("== E-mail inválido ==")
                    funcoes_gerais.linhaIgual("== E-mail inválido ==")
        elif  key == "5":
            print(f"== No momento a key 'cpf' tem valor {cliente['cpf']} ==")
            newKey = input("== Digite o novo valor da key 'cpf'. ==\n")
            
            if newKey.isdigit() == True and len(newKey) == 11:
                found = False

                for cliente in clientes:
                    if newKey == cliente['cpf']:
                        found = True

                        funcoes_gerais.linhaIgual("== Este CPF já está em uso. ==")
                        print("== Este CPF já está em uso. ==")
                        funcoes_gerais.linhaIgual("== Este CPF já está em uso. ==")
                        break
                if not found:
                    cliente.update({
                        "cpf": newKey
                    })
                    saveclient()
                    print(cliente)
                    funcoes_gerais.changedKey()
                    break
            else:
                funcoes_gerais.linhaIgual("== CPF inválido ==")
                print("== CPF inválido ==")
                funcoes_gerais.linhaIgual("== CPF inválido ==")
                continue
        elif  key == "6":
            print(f"== No momento a key 'pontos' tem valor {cliente['pontos']} ==")
            try:
                newKey = int(input("== Digite o novo valor da key 'pontos'. ==\n"))
            except ValueError:
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para a key. ==")
                print("== Você digitou um valor inválido para a key. ==")
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para a key. ==")
                continue
            if newKey < 0:
                funcoes_gerais.positiveOnly()
            else:
                cliente.update({
                    "pontos": newKey
                })
                saveclient()
                print(cliente)
                funcoes_gerais.changedKey()
                break
        else:
            funcoes_gerais.invalid(key)
            break

# Função 'alter()' consegue manipular valores das chaves dos dicionários de cada cliente e imprimir a alteração diretamente no documento do 'clientes.txt':
def alter():
    while True:
        loc = input("== Para realizar alteração, localize o cliente por seu nome ou número de identificação: ==\n"
        "Escolha um número:\n 1. Nome;\n 2. Número de identificação.\n"
            "Ou digite '0' para retornar.\n===========================\n")

        if loc == "1":
            nome_cliente = input("===Digite o nome do cliente:===\n")
            found = False

            for cliente in clientes:
                if nome_cliente == cliente["clienteNom"]:
                    found = True
                    key = input("== Qual chave do cliente deseja alterar? ==\n== Escolha um número: ==\n"
                    "1. Nome\n2. Número identificador\n3. Telefone\n4. E-mail\n5. CPF.\n6. Pontos.\n=============\n"
                    "== Ou digite qualquer outro comando para retornar ==\n=============\n")
                    att(key, cliente)
                    break
            if not found:
                funcoes_gerais.linhaIgual(f"== Cliente com nome '{nome_cliente}' não consta no cardápio. ==")
                print(f"== Cliente com nome '{nome_cliente}' não consta no cardápio. ==")
                funcoes_gerais.linhaIgual(f"== Cliente com nome '{nome_cliente}' não consta no cardápio. ==")
        elif loc == "2":
            try:
                id_cliente = int(input("== Digite o número de identificação: ==\n"))
            except ValueError:
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para o campo. ==")
                print("== Você digitou um valor inválido para o campo. ==")
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para o campo. ==")
            else:
                found = False

                for cliente in clientes:
                    if id_cliente == cliente["clienteID"]:
                        found = True
                        key = input("== Qual chave do cliente deseja alterar? ==\n== Escolha um número: ==\n"
                        "1. Nome\n2. Número identificador\n3. Telefone\n4. E-mail\n5. CPF.\n6. Pontos.\n=============\n"
                        "== Ou digite qualquer outro comando para retornar ==\n=============\n")
                        att(key, cliente)
                        break
                if not found:
                    funcoes_gerais.linhaIgual(f"== Cliente com número identificador '{id_cliente}' não consta no cardápio. ==")
                    print(f"== Cliente com número identificador '{id_cliente}' não consta no cardápio. ==")
                    funcoes_gerais.linhaIgual(f"== Cliente com número identificador '{id_cliente}' não consta no cardápio. ==")
        elif loc == "0":
                funcoes_gerais.back()
                break
        else:
            funcoes_gerais.invalid(loc)

# Função que remove clientes ao cardápio:
def remover():
    while True:            
        escolha = input("Como deseja remover o cliente?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação;\nOu digite '0' para retornar ao menu principal.\n")

        if escolha == "0":
            funcoes_gerais.back()
            break
        elif escolha == "1":
            nome_cliente = input("== Digite o nome do cliente: ==\n")
            found = False

            for cliente in clientes:
                if nome_cliente == cliente["clienteNom"]:
                    found = True

                    clientes.remove(cliente)

                    funcoes_gerais.linhaIgual(f"== Cliente {nome_cliente} removido. ==")
                    print(f"== Cliente {nome_cliente} removido. ==")
                    funcoes_gerais.linhaIgual(f"== Cliente {nome_cliente} removido. ==")
                    saveclient()
                    break
            if not found:
                funcoes_gerais.linhaIgual(f"== Cliente com nome '{nome_cliente}' já não existia entre os clientes. ==")
                print(f"== Cliente com nome '{nome_cliente}' já não existia entre os clientes. ==")
                funcoes_gerais.linhaIgual(f"== Cliente com nome '{nome_cliente}' já não existia entre os clientes. ==")
        elif escolha == "2":
            try:
                id_cliente = int(input("== Digite o número de identificação do cliente: ==\n"))
            except ValueError:
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para a key. ==")
                print("== Você digitou um valor inválido para a key. ==")
                funcoes_gerais.linhaIgual("== Você digitou um valor inválido para a key. ==")
            found = False

            for cliente in clientes:
                if id_cliente == cliente["clienteID"]:
                    found = True

                    clientes.remove(cliente)

                    funcoes_gerais.linhaIgual(f"== Cliente {id_cliente} removido. ==")
                    print(f"== Cliente {id_cliente} removido. ==")
                    funcoes_gerais.linhaIgual(f"== Cliente {id_cliente} removido. ==")
                    saveclient()
                    break
            if not found:
                funcoes_gerais.linhaIgual(f"== Cliente com número de identificação '{id_cliente}' já não existia entre os clientes. ==")
                print(f"== Cliente com número de identificação '{id_cliente}' já não existia entre os clientes. ==")
                funcoes_gerais.linhaIgual(f"== Cliente com número de identificação '{id_cliente}' já não existia entre os clientes. ==")
        else:
            funcoes_gerais.invalid(escolha)

# A função 'printClientes()' permite ao usuário visualizar toda a lista de clientes no terminal:
def printClentes():
    for cliente in clientes:
                print(f"> Nome: {cliente['clienteNom']};\n> Número identificador: {cliente['clienteID']};\n> Telefone: {cliente['telefone']};\n"
                f"> E-mail: {cliente['e-mail']};\n> CPF: {cliente['cpf']}\n> Pontos acumulados: {cliente['pontos']}\n====================")