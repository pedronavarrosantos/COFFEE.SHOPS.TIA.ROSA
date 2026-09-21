import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "CRUDs"))

import funcoes_gerais as fg
from db_connection_2 import get_connection

def localizar_ingrediente(coluna, valor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, ingrediente, quantidade FROM estoque WHERE {coluna} = %s", (valor,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return item

def atualizar_quantidade(ingrediente_id, ingrediente_nome, amount):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE estoque SET quantidade = %s WHERE id = %s", (amount, ingrediente_id))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"== Valor de {ingrediente_nome} atualizado para {amount}. ==")

def adicionar_ingrediente():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT MAX(id) FROM estoque")
    maior_id = cursor.fetchone()[0]
    novo_id = 0 if maior_id is None else maior_id + 1

    nome = input("== Digite o nome do novo ingrediente: ==\n")

    cursor.execute("SELECT id FROM estoque WHERE ingrediente = %s", (nome,))
    if cursor.fetchone():
        print("== Esse ingrediente já existe no estoque. ==\n")
        cursor.close()
        conn.close()
        return

    try:
        quantidade = int(input("== Digite a quantidade inicial: ==\n"))
    except ValueError:
        print("== Digite apenas números. ==\n")
        cursor.close()
        conn.close()
        return
    if quantidade < 0:
        fg.positiveOnly()
        cursor.close()
        conn.close()
        return

    cursor.execute(
        "INSERT INTO estoque (id, ingrediente, quantidade) VALUES (%s, %s, %s)",
        (novo_id, nome, quantidade)
    )
    conn.commit()
    print(f"== Ingrediente '{nome}' cadastrado com id {novo_id}. ==\n")

    cursor.close()
    conn.close()

def att():
    while True:
        escolha = input("Como deseja acessar o ingrediente?\nEscolha um número:\n1. Nome;\n2. Número de identificação.\n"
        "== Ou digite '0' para retornar ao menu principal. ==\n"
        "====================================================\n")
        if escolha == "1":
            ingNome = input("Digite o nome do ingrediente:\n")
            item = localizar_ingrediente("ingrediente", ingNome)
            if not item:
                fg.linhaIgual("== Ingrediente não encontrado. ==")
                print("== Ingrediente não encontrado. ==")
                fg.linhaIgual("== Ingrediente não encontrado. ==")
                continue
            try:
                amount = int(input("Digite a quantidade disponível do ingrediente:\n"))
            except ValueError:
                fg.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                print("== Você digitou um valor inválido. Digite apenas números. ==")
                fg.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                continue
            if amount < 0:
                fg.positiveOnly()
            else:
                atualizar_quantidade(item[0], item[1], amount)

        elif escolha == "2":
            try:
                ingId = int(input("Digite o número identificador do ingrediente:"))
            except ValueError:
                fg.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                print("== Você digitou um valor inválido. Digite apenas números. ==")
                fg.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                continue
            item = localizar_ingrediente("id", ingId)
            if not item:
                fg.linhaIgual("== Ingrediente não encontrado. ==")
                print("== Ingrediente não encontrado. ==")
                fg.linhaIgual("== Ingrediente não encontrado. ==")
                continue
            print(f"== O ingrediente com número identificador {ingId} é o(a) {item[1]}. ==")
            try:
                amount = int(input("Digite a quantidade disponível do ingrediente:"))
            except ValueError:
                fg.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                print("== Você digitou um valor inválido. Digite apenas números. ==")
                fg.linhaIgual("== Você digitou um valor inválido. Digite apenas números. ==")
                continue
            if amount < 0:
                fg.positiveOnly()
            else:
                atualizar_quantidade(item[0], item[1], amount)

        elif escolha == "0":
            fg.back()
            break
        else:
            fg.invalid(escolha)
def level():
    while True:
        escolha = input("Escolha uma opção:\n 1. Ver ingredientes em nível crítico;\n 2. Ver ingredientes em nível médio;\n"
        " 3. Ver ingredientes em quantidade segura;\n 4. Ver níveis de todos os ingredientes.\n"
        "== Ou digite '0' para retornar. ==\n"
        "==================================\n")

        conn = get_connection()
        cursor = conn.cursor()

        if escolha == "1":
            cursor.execute("SELECT ingrediente, quantidade FROM estoque WHERE quantidade <= 10 ORDER BY id")
            for ingrediente, quantidade in cursor.fetchall():
                if quantidade == 0:
                    print(f"== O estoque de {ingrediente} está zerado! ==\n== Dar urgência à reposição. ==")
                else:
                    print(f"== O estoque de {ingrediente} tem apenas {quantidade} unidades! ==\n== Dar prioridade à reposição. ==")
        elif escolha == "2":
            cursor.execute("SELECT ingrediente, quantidade FROM estoque WHERE quantidade BETWEEN 11 AND 50 ORDER BY id")
            for ingrediente, quantidade in cursor.fetchall():
                print(f"== O estoque de {ingrediente} tem {quantidade} unidades. ==\n== Reposição necessária em breve. ==")
        elif escolha == "3":
            cursor.execute("SELECT ingrediente, quantidade FROM estoque WHERE quantidade > 50 ORDER BY id")
            for ingrediente, quantidade in cursor.fetchall():
                print(f"== O estoque de {ingrediente} tem {quantidade} unidades. ==")
        elif escolha == "4":
            cursor.execute("SELECT ingrediente, quantidade FROM estoque ORDER BY id")
            for ingrediente, quantidade in cursor.fetchall():
                if quantidade <= 10:
                    if quantidade == 0:
                        print(f"== O estoque de {ingrediente} está zerado! ==\n== Dar urgência à reposição. ==")
                    else:
                        print(f"== O estoque de {ingrediente} tem apenas {quantidade} unidades! ==\n== Dar prioridade à reposição. ==")
                elif quantidade <= 50:
                    print(f"== O estoque de {ingrediente} tem {quantidade} unidades. ==\n== Reposição necessária em breve. ==")
                else:
                    print(f"== O estoque de {ingrediente} tem {quantidade} unidades. ==")
        elif escolha == "0":
            cursor.close()
            conn.close()
            fg.back()
            break
        else:
            fg.invalid(escolha)

        cursor.close()
        conn.close()

def showIng():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, ingrediente, quantidade FROM estoque ORDER BY id")
    for id_, ingrediente, quantidade in cursor.fetchall():
        print(f"{id_}. {ingrediente}; Quantidade: {quantidade}.")
    cursor.close()
    conn.close()