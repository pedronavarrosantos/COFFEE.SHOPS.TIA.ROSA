import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "GFUNCs"))

import funcoes_gerais as fg
from db_connection_2 import get_connection

def localizar_cliente(coluna, valor, apenas_ativos=True):
    conn = get_connection()
    cursor = conn.cursor()
    sql = f"SELECT id, nome, telefone, email, cpf, pontos, ativo FROM clientes WHERE {coluna} = %s"
    if apenas_ativos:
        sql += " AND ativo = TRUE"
    cursor.execute(sql, (valor,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    return cliente


def imprimir_cliente(cliente):
    print(f"== Nome: {cliente[1]}; ==\n== Número identificador: {cliente[0]}; ==\n== Telefone: {cliente[2]}; =="
          f"\n== E-mail: {cliente[3]}; ==\n== CPF: {cliente[4]}. ==\n== Pontos: {cliente[5]}. ==")
    print("======================")


def adicionar():
    while True:
        user = input("==================================================\n"
        "== Digite o nome do cliente ou 0 para retornar: ==\n"
        "==================================================\n")

        if user == "0":
            fg.back()
            break

        nTel = input("=============================================\n"
        "== Digite o número de telefone do cliente: ==\n"
        "=============================================\n")

        if not (nTel.isdigit() and len(nTel) in (9, 10, 11)):
            fg.linhaIgual("== Número de telefone inválido ==")
            print("== Número de telefone inválido ==")
            fg.linhaIgual("== Número de telefone inválido ==")
            continue

        e_mail = input("=================================\n"
        "== Digite o e-mail do cliente: ==\n"
        "=================================\n")

        if not ("@" in e_mail and e_mail[0] != "@" and e_mail.endswith(".com")):
            fg.linhaIgual("== E-mail inválido== ")
            print("== E-mail inválido== ")
            fg.linhaIgual("== E-mail inválido== ")
            continue

        cpf = input("==============================\n"
        "== Digite o CPF do cliente: ==\n"
        "==============================\n")

        if not (cpf.isdigit() and len(cpf) == 11):
            fg.linhaIgual("== CPF inválido ==")
            print("== CPF inválido ==")
            fg.linhaIgual("== CPF inválido ==")
            continue

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM clientes WHERE cpf = %s", (cpf,))
        if cursor.fetchone():
            fg.linhaIgual("== Este CPF já está em uso. ==")
            print("== Este CPF já está em uso. ==")
            fg.linhaIgual("== Este CPF já está em uso. ==")
            cursor.close(); conn.close()
            continue

        cursor.execute("SELECT MAX(id) FROM clientes")
        maior_id = cursor.fetchone()[0]
        userID = 1 if maior_id is None else maior_id + 1

        cursor.execute(
            "INSERT INTO clientes (id, nome, telefone, email, cpf, pontos) VALUES (%s, %s, %s, %s, %s, %s)",
            (userID, user, nTel, e_mail, cpf, 0)
        )
        conn.commit()
        cursor.close()
        conn.close()

        fg.linhaIgual(f"== Cliente com número identificador '{userID}' e nome '{user}' adicionado. ==")
        print(f"== Cliente com número identificador '{userID}' e nome '{user}' adicionado. ==")
        fg.linhaIgual(f"== Cliente com número identificador '{userID}' e nome '{user}' adicionado. ==")


def procurar():
    while True:
        escolha = input("Como deseja procurar o cliente?\nEscolha um número:\n"
        " 1. Nome\n 2. Número de identificação\n 3. Telefone\n 4. E-mail\n 5. CPF.\n"
        " Ou digite '0' para retornar.\n")

        if escolha == "1":
            valor = input("Digite o nome do cliente:\n")
            cliente = localizar_cliente("nome", valor)
        elif escolha == "2":
            try:
                valor = int(input("Digite o número de identificação do cliente:\n"))
            except ValueError:
                fg.linhaIgual("== ID inválido. Digite apenas números. ==")
                print("== ID inválido. Digite apenas números. ==")
                fg.linhaIgual("== ID inválido. Digite apenas números. ==")
                continue
            cliente = localizar_cliente("id", valor)
        elif escolha == "3":
            valor = input("Digite o telefone do cliente:\n")
            cliente = localizar_cliente("telefone", valor)
        elif escolha == "4":
            valor = input("Digite o e-mail do cliente:\n")
            cliente = localizar_cliente("email", valor)
        elif escolha == "5":
            valor = input("Digite o CPF do cliente:\n")
            cliente = localizar_cliente("cpf", valor)
        elif escolha == "0":
            fg.back()
            break
        else:
            fg.invalid(escolha)
            continue

        if not cliente:
            print("===========================")
            print("== Cliente não encontrado. ==")
            print("===========================\n")
        else:
            imprimir_cliente(cliente)


def att(key, cliente_id):
    conn = get_connection()
    cursor = conn.cursor()

    if key == "1":
        newKey = input("== Digite o novo valor do nome. ==\n")
        cursor.execute("UPDATE clientes SET nome = %s WHERE id = %s", (newKey, cliente_id))

    elif key == "3":
        newKey = input("== Digite o novo valor do telefone. ==\n")
        if not (newKey.isdigit() and 9 <= len(newKey) <= 11):
            fg.linhaIgual("== Número de telefone inválido ==")
            print("== Número de telefone inválido ==")
            fg.linhaIgual("== Número de telefone inválido ==")
            cursor.close(); conn.close(); return
        cursor.execute("UPDATE clientes SET telefone = %s WHERE id = %s", (newKey, cliente_id))

    elif key == "4":
        newKey = input("== Digite o novo valor do e-mail. ==\n")
        if not ("@" in newKey and newKey[0] != "@" and newKey.endswith(".com")):
            fg.linhaIgual("== E-mail inválido ==")
            print("== E-mail inválido ==")
            fg.linhaIgual("== E-mail inválido ==")
            cursor.close(); conn.close(); return
        cursor.execute("UPDATE clientes SET email = %s WHERE id = %s", (newKey, cliente_id))

    elif key == "5":
        newKey = input("== Digite o novo valor do CPF. ==\n")
        if not (newKey.isdigit() and len(newKey) == 11):
            fg.linhaIgual("== CPF inválido ==")
            print("== CPF inválido ==")
            fg.linhaIgual("== CPF inválido ==")
            cursor.close(); conn.close(); return
        cursor.execute("SELECT id FROM clientes WHERE cpf = %s AND id != %s", (newKey, cliente_id))
        if cursor.fetchone():
            fg.linhaIgual("== Este CPF já está em uso. ==")
            print("== Este CPF já está em uso. ==")
            fg.linhaIgual("== Este CPF já está em uso. ==")
            cursor.close(); conn.close(); return
        cursor.execute("UPDATE clientes SET cpf = %s WHERE id = %s", (newKey, cliente_id))

    elif key == "6":
        try:
            newKey = int(input("== Digite o novo valor de pontos. ==\n"))
        except ValueError:
            fg.linhaIgual("== Você digitou um valor inválido para a key. ==")
            print("== Você digitou um valor inválido para a key. ==")
            fg.linhaIgual("== Você digitou um valor inválido para a key. ==")
            cursor.close(); conn.close(); return
        if newKey < 0:
            fg.positiveOnly()
            cursor.close(); conn.close(); return
        cursor.execute("UPDATE clientes SET pontos = %s WHERE id = %s", (newKey, cliente_id))

    else:
        fg.invalid(key)
        cursor.close(); conn.close()
        return

    conn.commit()
    fg.changedKey()
    cursor.close()
    conn.close()


def alter():
    while True:
        loc = input("== Para realizar alteração, localize o cliente por seu nome ou número de identificação: ==\n"
        "Escolha um número:\n 1. Nome;\n 2. Número de identificação.\n"
            "Ou digite '0' para retornar.\n===========================\n")

        if loc == "1":
            nome_cliente = input("===Digite o nome do cliente:===\n")
            cliente = localizar_cliente("nome", nome_cliente)
        elif loc == "2":
            try:
                id_cliente = int(input("== Digite o número de identificação: ==\n"))
            except ValueError:
                fg.linhaIgual("== Você digitou um valor inválido para o campo. ==")
                print("== Você digitou um valor inválido para o campo. ==")
                fg.linhaIgual("== Você digitou um valor inválido para o campo. ==")
                continue
            cliente = localizar_cliente("id", id_cliente)
        elif loc == "0":
            fg.back()
            break
        else:
            fg.invalid(loc)
            continue

        if not cliente:
            print("=========================================================")
            print("== Cliente não consta na base. ==")
            print("=========================================================\n")
            continue

        key = input("== Qual chave do cliente deseja alterar? ==\n== Escolha um número: ==\n"
        "1. Nome\n3. Telefone\n4. E-mail\n5. CPF.\n6. Pontos.\n=============\n"
        "== Ou digite qualquer outro comando para retornar ==\n=============\n")
        att(key, cliente[0])


def remover():
    while True:
        escolha = input("Como deseja remover o cliente?\nEscolha um número:\n 1. Nome\n 2. Número de indentificação;\nOu digite '0' para retornar ao menu principal.\n")

        if escolha == "0":
            fg.back()
            break
        elif escolha == "1":
            nome_cliente = input("== Digite o nome do cliente: ==\n")
            cliente = localizar_cliente("nome", nome_cliente)
            remover_cliente(cliente, nome_cliente)
        elif escolha == "2":
            try:
                id_cliente = int(input("== Digite o número de identificação do cliente: ==\n"))
            except ValueError:
                fg.linhaIgual("== Você digitou um valor inválido para a key. ==")
                print("== Você digitou um valor inválido para a key. ==")
                fg.linhaIgual("== Você digitou um valor inválido para a key. ==")
                continue
            cliente = localizar_cliente("id", id_cliente)
            remover_cliente(cliente, id_cliente)
        else:
            fg.invalid(escolha)


def remover_cliente(cliente, referencia):
    if not cliente:
        print("=================================================================")
        print(f"== Cliente '{referencia}' já não existia entre os clientes. ==")
        print("=================================================================\n")
        return

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET ativo = FALSE WHERE id = %s", (cliente[0],))
    conn.commit()
    cursor.close()
    conn.close()

    print("===================================")
    print(f"== Cliente {referencia} removido. ==")
    print("===================================\n")


def reativar():
    while True:
        escolha = input("Como deseja localizar o cliente?\nEscolha um número:\n 1. Nome\n 2. Número de identificação;\nOu digite '0' para retornar.\n")

        if escolha == "0":
            fg.back()
            break
        elif escolha == "1":
            nome_cliente = input("== Digite o nome do cliente: ==\n")
            cliente = localizar_cliente("nome", nome_cliente, apenas_ativos=False)
        elif escolha == "2":
            try:
                id_cliente = int(input("== Digite o número de identificação do cliente: ==\n"))
            except ValueError:
                fg.linhaIgual("== Você digitou um valor inválido para a key. ==")
                print("== Você digitou um valor inválido para a key. ==")
                fg.linhaIgual("== Você digitou um valor inválido para a key. ==")
                continue
            cliente = localizar_cliente("id", id_cliente, apenas_ativos=False)
        else:
            fg.invalid(escolha)
            continue

        if not cliente:
            print("== Cliente não encontrado. ==\n")
            continue
        if cliente[6]:
            print("== Esse cliente já está ativo. ==\n")
            continue

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET ativo = TRUE WHERE id = %s", (cliente[0],))
        conn.commit()
        cursor.close()
        conn.close()

        print(f"== Cliente {cliente[1]} reativado. ==\n")

def showClients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, email, cpf, pontos FROM clientes WHERE ativo = TRUE ORDER BY id")
    for cliente in cursor.fetchall():
        print(f"> Nome: {cliente[1]};\n> Número identificador: {cliente[0]};\n> Telefone: {cliente[2]};\n"
        f"> E-mail: {cliente[3]}\n> CPF: {cliente[4]}\n> Pontos acumulados: {cliente[5]}\n====================")
    cursor.close()
    conn.close()