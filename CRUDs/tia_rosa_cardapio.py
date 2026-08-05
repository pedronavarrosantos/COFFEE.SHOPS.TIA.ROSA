"""
=== CRUD do cardápio do Coffee Shop da Tia Rosa. ===
-> O sistema conterá funções para o seguinte: Adicionar, procurar, alterar ou remover prato, impressão de todos os 
pratos do cardápio e impressão dos ingredientes de um prato.

-> Os pratos serão armazenados em dicionários com 5 chaves: nome, id (número identificador do prato), preço, ingredientes e descrição
"""

# Lista que receberá os dicionários de cada prato.
cardapio =[]
# Bloco de código que faz tratamento do dados no arquivo para serem inseridos na lista:
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
# Função 'invalid()' emite texto padrão em caso de invalidez de input, recebe como parâmetro a variável 'escolha', ou 'loc' ou 'options':
def invalid(escolha):
    print("=======================================")
    print(f"== O comando {escolha} não é válido. ==")
    print("===============================")
# Função 'back()' emite texto padrão para informar ao usuário que o programa está retornando ao menu principal:
def back():
    print("=================")
    print("== Retornando. ==")
    print("=================\n")
# Função 'changedKey()' emite texto padrão quando uma chave é alterada dentro da função 'att(key, prato)':
def changedKey():
    print("=================================")
    print("== Chave alterada com sucesso! ==")
    print("=================================")
# Função 'positiveOnly()' emite texto padrão quando o usuário tenta atribuir valor negativo a uma chave que só aceita valores positivos:
def positiveOnly():
    print("===================================================")
    print("== Essa variável aceita apenas valores positivos ==")
    print("===================================================\n")
# Função que adiciona pratos ao cardápio:
def adicionar():
    while True:

        rId = int(input("===================================================================\n"
        "== Digite o número de identificação do prato ou 0 para retornar: ==\n"
        "===================================================================\n"))

        if rId < 0:
            positiveOnly()
            continue
        if rId != 0:
            for prato in cardapio:
                if rId == int(prato["identificação"]):
                    print("================================================")
                    print("===Já existe um prato com essa identificação.===")
                    print("================================================\n")
                    break
            else:
                rNome = input("Digite o nome do prato:\n")
                rPreco = float(input("Digite o preço do prato:\n"))

                if rPreco < 0:
                    positiveOnly()
                    continue
                ingredientes = input("Digite os ingredientes:\n")
                rIngredientes = "'" + ingredientes + "'"
                descricao = input("Digite a descrição do prato:\n")
                rDescricao = "'" + descricao + "'"

                cardapio.append({
                    "identificação": rId,
                    "nome": rNome,
                    "preço": rPreco,
                    "ingredientes": rIngredientes,
                    "descrição": rDescricao
                })
                print(f"===Prato com número identificador '{rId}' e nome '{rNome}' adicionado ao cardápio.===")
                print("=================================================================================\n")
                savedoc()
        else:
            back()
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
                    print(f"===Identificação: {prato['identificação']};===\n===Nome: {prato['nome']};===\n===Preço: {prato['preço']};==="
                    f"\n===Ingredientes: {prato['ingredientes']};===\n===Descrição: {prato['descrição']}.===")
                    print("======================")

                    found = True
                    break
            if not found:
                        print("== Prato não encontrado. ==")
                        print("===========================\n")
        elif escolha == "2":
            id_prato = int(input("Digite o número de indentificação do prato:\n"))
            for prato in cardapio:
                if id_prato == prato["identificação"]:
                    print(f"== Identificação: {prato['identificação']}; ==\n== Nome: {prato['nome']}; ==\n== Preço: {prato['preço']}; =="
                    f"\n== Ingredientes: {prato['ingredientes']};===\n===Descrição: {prato['descrição']}. ==")
                    print("======================")

                    found = True
                    break
            if not found:
                        print("== Prato não encontrado. ==")
                        print("===========================\n")
        elif escolha == "0":
            back()
            break
        else:
            invalid(escolha)
# Função 'att()' funciona em conjunto com a função subsequente 'alter()';
# 'att()' serve para o usuário escolher qual chave de algum prato do cardapio deseja atualizar;
# Recebe como parâmetros as variáveis 'key' (presente em 'alter()') e 'prato'.
def att(key, prato):
    while True:
        if  key == "1":
            print(f"== No momento a key 'número de identificação' tem valor {prato['identificação']} ==")
            newKey = int(input("== Digite no novo valor da key 'identificação'. ==\n"))
            
            if newKey < 0:
                positiveOnly()
                continue
            found = False

            # O 'for'abaixo existe para evitar que, durante uma reatribuição da chave 'identificação', pratos fiquem com números identificadores repetidos.
            # O 'for' precisa ter uma variável diferente de 'prato', uma vez que a função já recebe um valor para essa variável, 
            # para isso, utiliza-se 'outro_prato":
            for outro_prato in cardapio:
                if outro_prato != prato:
                    if newKey == outro_prato["identificação"]:
                        found = True
                        print("== Outro prato já possui o número de identificação que você está tentando usar. ==")
                        print("==================================================================================")
                        continue
            if not found:
                prato.update({
                    "identificação": newKey
                })
                savedoc()
                print(prato)
                changedKey()
                break
        elif  key == "2":
            print(f"== No momento a key 'nome' tem valor {prato['nome']} ==")
            newKey = input("== Digite no novo valor da key 'nome'. ==\n")
            prato.update({
                "nome": newKey
            })
            savedoc()
            print(prato)
            changedKey()
            break
        elif  key == "3":
            print(f"== No momento a key 'preço' tem valor {prato['preço']} ==")
            newKey = float(input("== Digite no novo valor da key 'preço'. ==\n"))

            if newKey < 0:
                positiveOnly()
                continue
            prato.update({
                "preço": newKey
            })
            savedoc()
            print(prato)
            changedKey()
            break
        elif  key == "4":
            print(f"== No momento a key 'ingredientes' tem valor {prato['ingredientes']} ==")
            newKey = input("== Digite no novo valor da key 'ingredientes'. ==\n")
            prato.update({
                "ingredientes": newKey
            })
            savedoc()
            print(prato)
            changedKey()
            break
        elif  key == "5":
            print(f"== No momento a key 'descrição' tem valor {prato['descrição']} ==")
            newKey = input("== Digite no novo valor da key 'descrição'. ==\n")
            prato.update({
                "descrição": newKey
            })
            savedoc()
            print(prato)
            changedKey()
            break
            
        else:
            print(f"== O valor {key} é inválido. ==")
            print("=================================")
            continue
# Função 'alter()' consegue manipular valores das chaves dos dicionários de cada prato e imprimir a alteração diretamente no documento do 'cardapiotr,txt':
def alter():
    while True:
        loc = input("== Deseja localizar o prato pelo nome ou número de identificação? ==\n Escolha um número:\n 1. Nome;\n 2. Número de identificação.\n"
            "Ou digite '0' para retornar.\n===========================\n")

        if loc == "1":
            nome_prato = input("===Digite o nome do prato:===\n")
            found = False

            for prato in cardapio:
                if nome_prato == prato["nome"]:
                    found = True
                    key = input("== Qual chave do prato deseja alterar? ==\n== Escolha um número: ==\n"
                    "1. Número identificador\n2. Nome\n3. Preço\n4. Ingredientes\n5. Descrição.\n=============\n"
                    "== Ou digite qualquer outro comando para retornar ==\n=============")
                    att(key, prato)
                    break
            if not found:
                print(f"== Prato com nome '{nome_prato}' não consta no cardápio. ==")
                print("=========================================================\n")
        elif loc == "2":
            id_prato = int(input("===Digite o número de identificação:===\n"))
            found = False

            for prato in cardapio:
                if id_prato == prato["identificação"]:
                    found = True
                    key = input("== Qual chave do prato deseja alterar? ==\n== Escolha um número: ==\n"
                    "1. Número identificador\n2. Nome\n3. Preço\n4. Ingredientes\n5. Descrição.\n=============\n"
                    "== Ou digite qualquer outro comando para retornar ==\n=============")
                    att(key, prato)
                    break
            if not found:
                print(f"== Prato com nome '{id_prato}' não consta no cardápio. ==")
                print("=========================================================\n")
        elif loc == "0":
                back()
                break
        else:
            invalid(loc)
# Função que remove pratos ao cardápio:
def remover():
    while True:            
        escolha = input("Como deseja remover o prato?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação;\nOu digite '0' para retornar ao menu principal.\n")

        if escolha == "0":
            back()
            break
        elif escolha == "1":
            nome_prato = input("Digite o nome do prato:\n")
            found = False

            for prato in cardapio:
                if nome_prato == prato["nome"]:
                    found = True

                    cardapio.remove(prato)

                    print(f"== Prato {nome_prato} removido. ==")
                    print("===================================\n")
                    savedoc()
                    break
            if not found:
                print(f"== Prato com nome '{nome_prato}' já não existia no cardápio. ==")
                print("=================================================================\n")
        elif escolha == "2":
            id_prato = int(input("Digite o número de identificação do prato:\n"))
            found = False

            for prato in cardapio:
                if id_prato == prato["identificação"]:
                    found = True

                    cardapio.remove(prato)

                    print(f"== Prato {id_prato} removido. ==")
                    print("==================================\n")
                    savedoc()
                    break
            if not found:
                print(f"== Prato com número de identificação '{id_prato}' já não existia no cardápio. ==")
                print("==================================================================================\n")
        else:
            invalid(escolha)

# Bloco de código que contem todas as funcionalidades do CRUD:
while True:
    # A variável options permite navegar pelas funções do CRUD:
    options = input("Bem-vindo ao sistema de cardápio do Coffee Shops Tia Rosa\n"
    "Escolha um número de '1' a '6':\n"
    "1. Adicionar prato ao cardápio;\n2. Procurar prato no cardápio;\n3. Alterar dados de prato do cardápio;\n"
    "4. Remover prato do cardápio;\n5. Mostrar cardápio;\n6. Fechar sistema.\n")
    
    if options == "1":
        adicionar()
    elif options == "2":
        procurar()
    elif options == "3":
        alter()
    elif options == "4":
        remover()
    elif options == "5":
        for prato in cardapio:
            print(f"> Número identificador: {prato['identificação']};\n> Nome: {prato['nome']};\n> Preço: R$:{prato['preço']};\n"
            f"> Ingredientes: {prato['ingredientes']};\n> Descrição: {prato['descrição']}\n====================")
    elif options == "6":
        print("=====================================")
        print("== Encerrando sistema de cardápio. ==")
        print("=====================================")
        break
    else:
        invalid(options)