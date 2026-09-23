import sys
import os
import re

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "GFUNCs"))

import funcoes_gerais as fg
from db_connection_2 import get_connection

def localizar_cliente(coluna, valor, apenas_ativos=True):
    conn = get_connection()
    cursor = conn.cursor()
    # Incluindo 'idade' no SELECT (Posição 7)
    sql = f"SELECT id, nome, telefone, email, cpf, pontos, ativo, idade FROM clientes WHERE {coluna} = %s"
    if apenas_ativos:
        sql += " AND ativo = TRUE"
    cursor.execute(sql, (valor,))
    cliente = cursor.fetchone()
    cursor.close()
    conn.close()
    return cliente


def imprimir_cliente(cliente):
    # cliente[7] é a idade
    print(f"== Nome: {cliente[1]}; ==\n== Número identificador: {cliente[0]}; ==\n== Telefone: {cliente[2]}; =="
          f"\n== E-mail: {cliente[3]}; ==\n== CPF: {cliente[4]}. ==\n== Pontos: {cliente[5]}. ==\n== Idade: {cliente[7]} anos. ==")
    print("======================")


def adicionar():
    while True:
        user = input("==================================================\n"
        "== Digite o nome do cliente ou 0 para retornar: ==\n"
        "==================================================\n")

        if user == "0":
            fg.back()
            break

        # Solicitação de idade para cadastro manual
        try:
            idade = int(input("== Digite a idade do cliente: ==\n"))
            if idade < 0:
                fg.positiveOnly()
                continue
        except ValueError:
            print("== Digite apenas números para a idade. ==\n")
            continue

        nTel = input("== Digite o telefone do cliente: ==\n")
        if not (nTel.isdigit() and len(nTel) in (9, 10, 11)):
            fg.linhaIgual("== Telefone inválido =="); print("== Telefone inválido =="); fg.linhaIgual("== Telefone inválido =="); continue

        e_mail = input("== Digite o e-mail do cliente: ==\n")
        if not ("@" in e_mail and e_mail.endswith(".com")):
            fg.linhaIgual("== E-mail inválido =="); print("== E-mail inválido =="); fg.linhaIgual("== E-mail inválido =="); continue

        cpf = input("== Digite o CPF do cliente: ==\n")
        if not (cpf.isdigit() and len(cpf) == 11):
            fg.linhaIgual("== CPF inválido =="); print("== CPF inválido =="); fg.linhaIgual("== CPF inválido =="); continue

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM clientes WHERE cpf = %s", (cpf,))
        if cursor.fetchone():
            print("== CPF já em uso. =="); cursor.close(); conn.close(); continue

        cursor.execute("SELECT MAX(id) FROM clientes")
        maior_id = cursor.fetchone()[0]
        userID = 1 if maior_id is None else maior_id + 1

        # Inserindo idade no banco de dados
        cursor.execute(
            "INSERT INTO clientes (id, nome, telefone, email, cpf, pontos, idade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (userID, user, nTel, e_mail, cpf, 0, idade)
        )
        conn.commit()
        cursor.close(); conn.close()

        print(f"== Cliente {user} cadastrado com ID {userID}! ==")


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
                print("== ID inválido. =="); continue
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
            print("== Cliente não encontrado. ==\n")
        else:
            imprimir_cliente(cliente)


def att(key, cliente_id):
    conn = get_connection()
    cursor = conn.cursor()

    if key == "1":
        newVal = input("Novo nome: ")
        cursor.execute("UPDATE clientes SET nome = %s WHERE id = %s", (newVal, cliente_id))
    elif key == "3":
        newVal = input("Novo telefone: ")
        cursor.execute("UPDATE clientes SET telefone = %s WHERE id = %s", (newVal, cliente_id))
    elif key == "4":
        newVal = input("Novo e-mail: ")
        cursor.execute("UPDATE clientes SET email = %s WHERE id = %s", (newVal, cliente_id))
    elif key == "5":
        newVal = input("Novo CPF: ")
        cursor.execute("UPDATE clientes SET cpf = %s WHERE id = %s", (newVal, cliente_id))
    elif key == "6":
        try:
            newVal = int(input("Novos pontos: "))
            cursor.execute("UPDATE clientes SET pontos = %s WHERE id = %s", (newVal, cliente_id))
        except ValueError: print("Valor inválido"); cursor.close(); conn.close(); return
    elif key == "7": # Atualizar a Idade
        try:
            newVal = int(input("Nova idade: "))
            cursor.execute("UPDATE clientes SET idade = %s WHERE id = %s", (newVal, cliente_id))
        except ValueError: print("Valor inválido"); cursor.close(); conn.close(); return
    else:
        fg.invalid(key)
        cursor.close(); conn.close()
        return

    conn.commit()
    fg.changedKey()
    cursor.close(); conn.close()


def remover():
    while True:
        escolha = input("Como deseja remover o cliente?\nEscolha um número:\n 1. Nome\n 2. Número de identificação;\nOu digite '0' para retornar.\n")
        if escolha == "0":
            fg.back()
            break
        elif escolha == "1":
            nome_cliente = input("Nome do cliente: ")
            cliente = localizar_cliente("nome", nome_cliente)
            remover_cliente(cliente, nome_cliente)
        elif escolha == "2":
            try:
                id_cliente = int(input("ID do cliente: "))
            except ValueError:
                print("ID inválido"); continue
            cliente = localizar_cliente("id", id_cliente)
            remover_cliente(cliente, id_cliente)
        else:
            fg.invalid(escolha)
            continue

def remover_cliente(cliente, referencia):
    if not cliente:
        print(f"== Cliente '{referencia}' não existe. ==")
        return
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE clientes SET ativo = FALSE WHERE id = %s", (cliente[0],))
    conn.commit()
    cursor.close(); conn.close()
    print(f"== Cliente {referencia} removido. ==")


def reativar():
    while True:
        escolha = input("Como deseja localizar o cliente?\nEscolha um número:\n 1. Nome\n 2. Número de identificação;\nOu digite '0' para retornar.\n")
        if escolha == "1":
            nome_cliente = input("Nome do cliente: ")
            cliente = localizar_cliente("nome", nome_cliente, apenas_ativos=False)
        elif escolha == "2":
            try:
                id_cliente = int(input("ID do cliente: "))
            except ValueError:
                print("ID inválido"); continue
            cliente = localizar_cliente("id", id_cliente, apenas_ativos=False)
        elif escolha == "0":
            fg.back()
            break
        else:
            fg.invalid(escolha)
            continue

        if not cliente:
            print("== Cliente não encontrado. ==\n")
            continue
        if cliente[6]:
            print("== Este cliente já está ativo. ==\n")
            continue

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE clientes SET ativo = TRUE WHERE id = %s", (cliente[0],))
        conn.commit()
        cursor.close(); conn.close()
        print(f"== Cliente {cliente[1]} reativado. ==\n")

def showClients():
    conn = get_connection()
    cursor = conn.cursor()
    # SELECT atualizado para incluir idade
    cursor.execute("SELECT id, nome, telefone, email, cpf, pontos, idade FROM clientes WHERE ativo = TRUE ORDER BY id")
    for cliente in cursor.fetchall():
        print(f"> Nome: {cliente[1]} | ID: {cliente[0]} | Idade: {cliente[6]} | Pontos: {cliente[5]}")
    cursor.close()
    conn.close()

# FUNÇÃO PARA A IA
def adicionar_cliente_automatico(nome, telefone, email, cpf, idade):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cpf_limpo = re.sub(r'\D', '', cpf)
        telefone_limpo = re.sub(r'\D', '', telefone)

        if len(cpf_limpo) != 11:
            return False, f"CPF inválido gerado pela IA: '{cpf}'"

        cursor.execute("SELECT id FROM clientes WHERE cpf = %s", (cpf_limpo,))
        if cursor.fetchone():
            return False, "CPF já cadastrado"

        cursor.execute("SELECT id FROM clientes WHERE email = %s", (email,))
        if cursor.fetchone():
            return False, "E-mail já cadastrado"

        cursor.execute("SELECT MAX(id) FROM clientes")
        maior_id = cursor.fetchone()[0]
        userID = 1 if maior_id is None else maior_id + 1
        cursor.execute(
            "INSERT INTO clientes (id, nome, telefone, email, cpf, pontos, idade) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (userID, nome, telefone_limpo, email, cpf_limpo, 0, idade)
        )
        conn.commit()
        return True, userID
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cursor.close(); conn.close()