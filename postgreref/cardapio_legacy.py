from db_connection_2 import get_connection

def mostrar():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, preco, descricao FROM cardapio ORDER by id")
    pratos = cursor.fetchall()

    for prato in pratos:
        print(f"> Número identificador: {prato[0]};\n"
        f"> Nome: {prato[1]};\n"
        f"> Preço: R$:{prato[2]};\n"
        f"> Descrição: {prato[3]}")
        linhaIgual(f"> Descrição: {prato[3]}")

    cursor.close()
    conn.close()

def linhaIgual(x):
    lin = len(x)
    print("=" * lin)
# Função 'invalid()' emite texto padrão em caso de invalidez de input, recebe como parâmetro a variável 'escolha', ou 'loc' ou 'options':
def invalid(escolha):
    print("=================================")
    print(f"== O comando '{escolha}' não é válido. ==")
    print("=================================")
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

def mostrar_ingredientes_disponiveis(cursor):
    cursor.execute("SELECT id, ingrediente FROM estoque ORDER BY id")
    itens = cursor.fetchall()
    print("== Ingredientes disponíveis: ==")
    for item in itens:
        print(f"{item[0]} - {item[1]}")
    print()


def adicionar_ingredientes_ao_prato(cursor, conn, cardapio_id):
    while True:
        mostrar_ingredientes_disponiveis(cursor)
        entrada = input("== Digite o ID do ingrediente para adicionar ao prato, ou 0 para finalizar: ==\n")
        estoque_id = int(entrada)

        if estoque_id == 0:
            break

        cursor.execute("SELECT id FROM estoque WHERE id = %s", (estoque_id,))
        existe = cursor.fetchone()

        if not existe:
            print("======================================")
            print("== Esse ID não existe no estoque. ==")
            print("======================================\n")
            continue

        cursor.execute(
            "INSERT INTO cardapio_ingredientes (cardapio_id, estoque_id) VALUES (%s, %s)",
            (cardapio_id, estoque_id)
        )
        conn.commit()
        print("== Ingrediente adicionado ao prato. ==\n")
# Função que adiciona pratos ao cardápio:
def adicionar():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(id) FROM cardapio")
    maior_id = cursor.fetchone()[0]

    rId = 1 if maior_id is None else maior_id + 1

    rNome = input("== Digite o nome do prato: ==\n")
    rPreco = float(input("== Digite o preço do prato: ==\n"))

    if rPreco < 0:
        positiveOnly()
        cursor.close()
        conn.close()
        return

    descricao = input("== Digite a descrição do prato: ==\n")

    cursor.execute(
        "INSERT INTO cardapio (id, nome, preco, descricao) VALUES (%s, %s, %s, %s)",
        (rId, rNome, rPreco, descricao)
    )
    conn.commit()

    print("=================================================================================")
    print(f"== Prato com número identificador '{rId}' e nome '{rNome}' adicionado ao cardápio. ==")
    print("=================================================================================\n")

    adicionar_ingredientes_ao_prato(cursor, conn, rId)

    cursor.close()
    conn.close()
# Função que procura pratos ao cardápio:
def procurar():
    while True:
        escolha = input("Como deseja procurar o prato?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação.\n Ou digite '0' para retornar.\n")

        if escolha == "1":
            nome_prato = input("Digite o nome do prato:\n")
            buscar_e_exibir_prato(coluna="nome", valor=nome_prato)

        elif escolha == "2":
            entrada = input("Digite o número de indentificação do prato:\n")
            try:
                id_prato = int(entrada)
            except ValueError:
                print("===================================")
                print("== Digite apenas números válidos. ==")
                print("===================================\n")
                continue
            buscar_e_exibir_prato(coluna="id", valor=id_prato)

        elif escolha == "0":
            back()
            break
        else:
            invalid(escolha)


def buscar_e_exibir_prato(coluna, valor):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"SELECT id, nome, preco, descricao FROM cardapio WHERE {coluna} = %s", (valor,))
    prato = cursor.fetchone()

    if not prato:
        print("===========================")
        print("== Prato não encontrado. ==")
        print("===========================\n")
        cursor.close()
        conn.close()
        return

    cursor.execute(
        "SELECT e.ingrediente FROM cardapio_ingredientes ci "
        "JOIN estoque e ON ci.estoque_id = e.id "
        "WHERE ci.cardapio_id = %s",
        (prato[0],)
    )
    ingredientes = [linha[0] for linha in cursor.fetchall()]
    ingredientes_texto = ", ".join(ingredientes)

    print(f"== Identificação: {prato[0]}; ==\n== Nome: {prato[1]}; ==\n== Preço: {prato[2]}; =="
          f"\n== Ingredientes: {ingredientes_texto}; ==\n== Descrição: {prato[3]}. ==")
    print("======================")

    cursor.close()
    conn.close()
    
def localizar_prato(coluna, valor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, nome, preco, descricao FROM cardapio WHERE {coluna} = %s", (valor,))
    prato = cursor.fetchone()
    cursor.close()
    conn.close()
    return prato


def att(key, prato_id):
    conn = get_connection()
    cursor = conn.cursor()

    if key == "2":
        newKey = input("== Digite o novo valor da key 'nome'. ==\n")
        cursor.execute("UPDATE cardapio SET nome = %s WHERE id = %s", (newKey, prato_id))

    elif key == "3":
        try:
            newKey = float(input("== Digite o novo valor da key 'preço'. ==\n"))
        except ValueError:
            print("== Digite apenas números válidos. ==")
            cursor.close(); conn.close(); return
        if newKey < 0:
            positiveOnly()
            cursor.close(); conn.close(); return
        cursor.execute("UPDATE cardapio SET preco = %s WHERE id = %s", (newKey, prato_id))

    elif key == "4":
        cursor.execute("DELETE FROM cardapio_ingredientes WHERE cardapio_id = %s", (prato_id,))
        conn.commit()
        adicionar_ingredientes_ao_prato(cursor, conn, prato_id)
        cursor.close(); conn.close()
        changedKey()
        return

    elif key == "5":
        newKey = input("== Digite o novo valor da key 'descrição'. ==\n")
        cursor.execute("UPDATE cardapio SET descricao = %s WHERE id = %s", (newKey, prato_id))

    else:
        invalid(key)
        cursor.close(); conn.close()
        return

    conn.commit()
    changedKey()
    cursor.close()
    conn.close()


def alter():
    while True:
        loc = input("== Para realizar alteração, localize o prato por seu nome ou número de identificação: ==\n"
        "Escolha um número:\n 1. Nome;\n 2. Número de identificação.\n"
            "Ou digite '0' para retornar.\n===========================\n")

        if loc == "1":
            nome_prato = input("===Digite o nome do prato:===\n")
            prato = localizar_prato("nome", nome_prato)
        elif loc == "2":
            try:
                id_prato = int(input("== Digite o número de identificação: ==\n"))
            except ValueError:
                print("== Esse campo aceita apenas números inteiros. ==")
                continue
            prato = localizar_prato("id", id_prato)
        elif loc == "0":
            back()
            break
        else:
            invalid(loc)
            continue

        if not prato:
            print("=========================================")
            print("== Prato não consta no cardápio. ==")
            print("=========================================\n")
            continue

        key = input("== Qual chave do prato deseja alterar? ==\n== Escolha um número: ==\n"
        "2. Nome\n3. Preço\n4. Ingredientes\n5. Descrição.\n=============\n"
        "== Ou digite qualquer outro comando para retornar ==\n=============\n")
        att(key, prato[0])
# Função que remove pratos ao cardápio:
def remover():
    while True:            
        escolha = input("Como deseja remover o prato?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação;\nOu digite '0' para retornar ao menu principal.\n")

        if escolha == "0":
            back()
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
            invalid(escolha)

# A função responsável por executar o sistema do cardápio no arquivo 'main.py':
def sistema_cardapio():
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
            mostrar()
        elif options == "6":
            print("=====================================")
            print("== Encerrando sistema de cardápio. ==")
            print("=====================================")
            break
        else:
            invalid(options)

if __name__ == "__main__":
    sistema_cardapio()