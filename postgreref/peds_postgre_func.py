import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "GFUNCs"))

import funcoes_gerais as fg
from db_connection_2 import get_connection

def buscar_cliente(cursor, valor):
    cursor.execute(
        "SELECT id, nome, pontos FROM clientes WHERE ativo = TRUE AND (nome = %s OR CAST(id AS TEXT) = %s)",
        (valor, valor)
    )
    return cursor.fetchone()


def buscar_prato(cursor, valor):
    cursor.execute(
        "SELECT id, nome, preco FROM cardapio WHERE ativo = TRUE AND (nome = %s OR CAST(id AS TEXT) = %s)",
        (valor, valor)
    )
    return cursor.fetchone()


def ingredientes_do_prato(cursor, cardapio_id):
    cursor.execute(
        "SELECT e.id, e.ingrediente, e.quantidade FROM cardapio_ingredientes ci "
        "JOIN estoque e ON ci.estoque_id = e.id WHERE ci.cardapio_id = %s",
        (cardapio_id,)
    )
    return cursor.fetchall()


def adicionar():
    conn = get_connection()
    cursor = conn.cursor()

    cliente_encontrado = None
    while True:
        cliente_input = input("Digite o nome do cliente ou o seu número identificador:\n== Ou digite '0' para retornar. ==\n")
        if cliente_input == "0":
            fg.back()
            cursor.close(); conn.close()
            return
        cliente_encontrado = buscar_cliente(cursor, cliente_input)
        if cliente_encontrado is None:
            fg.linhaIgual("== Cliente não encontrado. ==")
            print("== Cliente não encontrado. ==")
            fg.linhaIgual("== Cliente não encontrado. ==")
            continue
        print(f"Cliente número {cliente_encontrado[0]}, nome: {cliente_encontrado[1]}.\n")
        break

    itens_pedido = []
    reservas = {}
    preco_total = 0

    while True:
        produto = input("Digite o nome do prato ou o seu número identificador:\n== Ou digite '0' para finalizar o pedido. ==\n")
        if produto == "0":
            break

        prato = buscar_prato(cursor, produto)
        if prato is None:
            print("== Prato não encontrado. ==")
            continue

        try:
            quantidade = int(input("Digite a quantidade do prato:\n"))
        except ValueError:
            print("== Digite apenas números inteiros. ==")
            continue
        if quantidade <= 0:
            print("== Esse campo aceita apenas valores inteiros positivos. ==")
            continue

        ingredientes = ingredientes_do_prato(cursor, prato[0])
        faltando = []
        for estoque_id, nome_ing, disponivel in ingredientes:
            necessario = quantidade + reservas.get(estoque_id, 0)
            if necessario > disponivel:
                faltando.append((nome_ing, max(disponivel - reservas.get(estoque_id, 0), 0)))

        if faltando:
            fg.linhaIgual("== Estoque insuficiente para este prato. ==")
            print("== Estoque insuficiente para este prato. ==")
            for nome_ing, sobra in faltando:
                print(f"   - Falta '{nome_ing}': disponível apenas {sobra} unidade(s).")
            fg.linhaIgual("== Estoque insuficiente para este prato. ==")
            continue

        for estoque_id, _, _ in ingredientes:
            reservas[estoque_id] = reservas.get(estoque_id, 0) + quantidade

        itens_pedido.append((prato[0], prato[1], prato[2], quantidade))
        preco_total += prato[2] * quantidade
        print(f"== '{prato[1]}' (x{quantidade}) adicionado ao pedido. ==")

    if not itens_pedido:
        print("== Pedido cancelado: nenhum prato foi adicionado. ==")
        cursor.close(); conn.close()
        return

    try:
        for estoque_id, qtd_usada in reservas.items():
            cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE id = %s", (qtd_usada, estoque_id))

        cliente_id, cliente_nome, pontos = cliente_encontrado
        desconto = pontos >= 5
        preco_final = preco_total * 0.85 if desconto else preco_total

        cursor.execute("SELECT MAX(id) FROM pedidos")
        maior_id = cursor.fetchone()[0]
        id_pedido = 100 if maior_id is None else maior_id + 1

        cursor.execute(
            "INSERT INTO pedidos (id, cliente_id, valor_total, status) VALUES (%s, %s, %s, %s)",
            (id_pedido, cliente_id, preco_final, "em andamento")
        )

        for cardapio_id, _, _, quantidade in itens_pedido:
            cursor.execute(
                "INSERT INTO pedido_itens (pedido_id, cardapio_id, quantidade) VALUES (%s, %s, %s)",
                (id_pedido, cardapio_id, quantidade)
            )

        if desconto:
            cursor.execute("UPDATE clientes SET pontos = pontos - 5 WHERE id = %s", (cliente_id,))

        conn.commit()
    except Exception as erro:
        conn.rollback()
        print(f"== Ocorreu um erro e o pedido não foi criado: {erro} ==")
        cursor.close(); conn.close()
        return

    cursor.close()
    conn.close()

    if desconto:
        valor_desc = preco_total - preco_final
        fg.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! ==")
        print(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_final:.2f} ==")
        fg.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! ==")
        print(f"== Esse pedido teve o desconto de fidelidade. ==\n== Valor sem desconto R$ {preco_total:.2f}, valor com desconto R$ {preco_final:.2f} ==\n"
              f"Valor do desconto: R$ {valor_desc:.2f}.")
    else:
        fg.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_final:.2f} ==")
        print(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_final:.2f} ==")
        fg.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_final:.2f} ==")


def verificar():
    while True:
        id_pedido = input("== Digite o número do pedido que deseja verificar: ==\n== Ou digite '0' para retornar. ==\n")
        if id_pedido == "0":
            fg.back()
            break
        try:
            id_pedido_int = int(id_pedido)
        except ValueError:
            print("== Esse campo aceita apenas números inteiros. ==")
            continue

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM pedidos WHERE id = %s", (id_pedido_int,))
        resultado = cursor.fetchone()
        cursor.close()
        conn.close()

        print(f"== O pedido está {resultado[0]}. ==" if resultado else f"== O pedido {id_pedido_int} não existe. ==")


def listar_pratos_do_pedido(cursor, pedido_id):
    cursor.execute(
        "SELECT pi.id, c.nome, pi.quantidade FROM pedido_itens pi "
        "JOIN cardapio c ON pi.cardapio_id = c.id WHERE pi.pedido_id = %s ORDER BY pi.id",
        (pedido_id,)
    )
    itens = cursor.fetchall()
    for i, item in enumerate(itens):
        print(f"  {i + 1}. {item[1]} (x{item[2]})")
    return itens


def escolher_item_do_pedido(cursor, pedido_id):
    itens = listar_pratos_do_pedido(cursor, pedido_id)
    if not itens:
        print("== Este pedido não tem pratos. ==")
        return None
    escolha = input("Digite o número da linha do prato:\n== Ou digite '0' para cancelar. ==\n")
    if escolha == "0":
        return None
    try:
        indice = int(escolha) - 1
    except ValueError:
        print("== Digite apenas números inteiros. ==")
        return None
    if indice < 0 or indice >= len(itens):
        print("== Número de linha inválido. ==")
        return None
    return itens[indice]


def adicionar_prato_ao_pedido(cursor, conn, pedido_id):
    produto = input("Digite o nome do prato ou o seu número identificador a adicionar:\n== Ou digite '0' para cancelar. ==\n")
    if produto == "0":
        return
    prato = buscar_prato(cursor, produto)
    if prato is None:
        print("== Prato não encontrado. ==")
        return
    try:
        quantidade = int(input("Digite a quantidade do prato:\n"))
    except ValueError:
        print("== Digite apenas números inteiros. ==")
        return
    if quantidade <= 0:
        print("== Esse campo aceita apenas valores inteiros positivos. ==")
        return

    ingredientes = ingredientes_do_prato(cursor, prato[0])
    faltando = [(nome, disp) for _, nome, disp in ingredientes if disp < quantidade]
    if faltando:
        fg.linhaIgual("== Estoque insuficiente para este prato. ==")
        print("== Estoque insuficiente para este prato. ==")
        for nome, disp in faltando:
            print(f"   - Falta '{nome}': disponível apenas {disp} unidade(s).")
        fg.linhaIgual("== Estoque insuficiente para este prato. ==")
        return

    try:
        for estoque_id, _, _ in ingredientes:
            cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE id = %s", (quantidade, estoque_id))
        cursor.execute("INSERT INTO pedido_itens (pedido_id, cardapio_id, quantidade) VALUES (%s, %s, %s)", (pedido_id, prato[0], quantidade))
        cursor.execute("UPDATE pedidos SET valor_total = valor_total + %s WHERE id = %s", (prato[2] * quantidade, pedido_id))
        conn.commit()
    except Exception as erro:
        conn.rollback()
        print(f"== Ocorreu um erro: {erro} ==")
        return

    print(f"== '{prato[1]}' (x{quantidade}) adicionado ao pedido nº {pedido_id}. ==")


def remover_prato_do_pedido(cursor, conn, pedido_id):
    item = escolher_item_do_pedido(cursor, pedido_id)
    if item is None:
        return
    pedido_item_id, nome, quantidade = item

    cursor.execute("SELECT cardapio_id, c.preco FROM pedido_itens pi JOIN cardapio c ON pi.cardapio_id = c.id WHERE pi.id = %s", (pedido_item_id,))
    cardapio_id, preco = cursor.fetchone()
    ingredientes = ingredientes_do_prato(cursor, cardapio_id)

    try:
        for estoque_id, _, _ in ingredientes:
            cursor.execute("UPDATE estoque SET quantidade = quantidade + %s WHERE id = %s", (quantidade, estoque_id))
        cursor.execute("DELETE FROM pedido_itens WHERE id = %s", (pedido_item_id,))
        cursor.execute("UPDATE pedidos SET valor_total = valor_total - %s WHERE id = %s", (preco * quantidade, pedido_id))
        conn.commit()
    except Exception as erro:
        conn.rollback()
        print(f"== Ocorreu um erro: {erro} ==")
        return

    print(f"== '{nome}' removido do pedido nº {pedido_id}. ==")


def alterar_quantidade_no_pedido(cursor, conn, pedido_id):
    item = escolher_item_do_pedido(cursor, pedido_id)
    if item is None:
        return
    pedido_item_id, nome, quantidade_antiga = item

    cursor.execute("SELECT cardapio_id, c.preco FROM pedido_itens pi JOIN cardapio c ON pi.cardapio_id = c.id WHERE pi.id = %s", (pedido_item_id,))
    cardapio_id, preco = cursor.fetchone()

    try:
        quantidade_nova = int(input("Digite a nova quantidade:\n"))
    except ValueError:
        print("== Digite apenas números inteiros. ==")
        return
    if quantidade_nova <= 0:
        print("== Esse campo aceita apenas valores inteiros positivos. Use a opção de remover se quiser tirar o prato do pedido. ==")
        return

    diferenca = quantidade_nova - quantidade_antiga
    ingredientes = ingredientes_do_prato(cursor, cardapio_id)

    if diferenca > 0:
        faltando = [(nome_ing, disp) for _, nome_ing, disp in ingredientes if disp < diferenca]
        if faltando:
            fg.linhaIgual("== Estoque insuficiente para aumentar a quantidade. ==")
            print("== Estoque insuficiente para aumentar a quantidade. ==")
            for nome_ing, disp in faltando:
                print(f"   - Falta '{nome_ing}': disponível apenas {disp} unidade(s) a mais.")
            fg.linhaIgual("== Estoque insuficiente para aumentar a quantidade. ==")
            return

    try:
        for estoque_id, _, _ in ingredientes:
            cursor.execute("UPDATE estoque SET quantidade = quantidade - %s WHERE id = %s", (diferenca, estoque_id))
        cursor.execute("UPDATE pedido_itens SET quantidade = %s WHERE id = %s", (quantidade_nova, pedido_item_id))
        cursor.execute("UPDATE pedidos SET valor_total = valor_total + %s WHERE id = %s", (preco * diferenca, pedido_id))
        conn.commit()
    except Exception as erro:
        conn.rollback()
        print(f"== Ocorreu um erro: {erro} ==")
        return

    print(f"== Quantidade de '{nome}' alterada de {quantidade_antiga} para {quantidade_nova}. ==")


def modificar_pedido():
    conn = get_connection()
    cursor = conn.cursor()

    pedido_id = None
    while True:
        localizar = input("Qual o número do pedido que deseja modificar?\n== Ou digite '0' para retornar. ==\n")
        if localizar == "0":
            fg.back()
            cursor.close(); conn.close()
            return
        try:
            id_busca = int(localizar)
        except ValueError:
            print("Esse campo aceita apenas números inteiros.")
            continue

        cursor.execute("SELECT id, status FROM pedidos WHERE id = %s", (id_busca,))
        pedido = cursor.fetchone()
        if pedido is None:
            print("== Pedido não encontrado. ==")
            continue
        if pedido[1] != "em andamento":
            print(f"== Este pedido está '{pedido[1]}' e não pode mais ser modificado. ==")
            continue
        pedido_id = pedido[0]
        break

    while True:
        cursor.execute("SELECT valor_total FROM pedidos WHERE id = %s", (pedido_id,))
        valor_total = cursor.fetchone()[0]
        print(f"\n== Pedido nº {pedido_id} — Total atual: R$ {valor_total:.2f} ==")

        escolha = input(
            "O que deseja fazer?\n1. Adicionar prato;\n2. Remover prato;\n3. Alterar quantidade de um prato;\n"
            "== Ou digite '0' para retornar ao menu principal. ==\n"
        )

        if escolha == "0":
            fg.back()
            break
        elif escolha == "1":
            adicionar_prato_ao_pedido(cursor, conn, pedido_id)
        elif escolha == "2":
            remover_prato_do_pedido(cursor, conn, pedido_id)
        elif escolha == "3":
            alterar_quantidade_no_pedido(cursor, conn, pedido_id)
        else:
            fg.invalid(escolha)

    cursor.close()
    conn.close()


def entrega():
    while True:
        localizar_pedido = input("== Qual pedido será entregue? ==\n== Caso queira retornar ao menu principal digite '0'. ==\n")
        if localizar_pedido == "0":
            fg.back()
            break
        try:
            id_pedido_busca = int(localizar_pedido)
        except ValueError:
            print("Esse campo aceita apenas números inteiros.")
            continue

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM pedidos WHERE id = %s", (id_pedido_busca,))
        resultado = cursor.fetchone()

        if resultado is None:
            print("== Pedido não encontrado. ==")
        elif resultado[0] == "em andamento":
            cursor.execute("UPDATE pedidos SET status = 'feito' WHERE id = %s", (id_pedido_busca,))
            conn.commit()
            print(f"== Pedido nº {id_pedido_busca} marcado como 'feito'. ==")
        else:
            print("== O pedido não pode ser entregue por não se encontrar em fase de andamento. ==")

        cursor.close()
        conn.close()


def cancelar():
    while True:
        id_pedido = input("== Digite o número do pedido que deseja cancelar: ==\n== Ou digite '0' para retornar. ==\n")
        if id_pedido == "0":
            fg.back()
            break
        try:
            id_pedido_int = int(id_pedido)
        except ValueError:
            print("== Esse campo aceita apenas números inteiros. ==")
            continue

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM pedidos WHERE id = %s", (id_pedido_int,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(f"== O pedido de número {id_pedido_int} não foi encontrado. ==")
            cursor.close(); conn.close()
            continue
        if resultado[0] != "em andamento":
            print(f"== O pedido de número {id_pedido_int} já superou a fase de andamento e não pode mais ser cancelado. ==")
            cursor.close(); conn.close()
            continue

        escolha = input("== Realmente deseja cancelar o pedido? ==\n== Escolha um número: ==\n1. Sim\n2. Não\n")

        if escolha == "1":
            cursor.execute("SELECT cardapio_id, quantidade FROM pedido_itens WHERE pedido_id = %s", (id_pedido_int,))
            itens = cursor.fetchall()
            try:
                for cardapio_id, quantidade in itens:
                    for estoque_id, _, _ in ingredientes_do_prato(cursor, cardapio_id):
                        cursor.execute("UPDATE estoque SET quantidade = quantidade + %s WHERE id = %s", (quantidade, estoque_id))
                cursor.execute("UPDATE pedidos SET status = 'cancelado' WHERE id = %s", (id_pedido_int,))
                conn.commit()
                print(f"== Pedido {id_pedido_int} cancelado. ==")
            except Exception as erro:
                conn.rollback()
                print(f"== Ocorreu um erro: {erro} ==")
        elif escolha == "2":
            fg.back()

        cursor.close()
        conn.close()


def fechar():
    while True:
        id_pedido = input("== Digite o número do pedido que deseja fechar: ==\n== Ou digite '0' para retornar. ==\n")
        if id_pedido == "0":
            fg.back()
            break
        try:
            id_pedido_int = int(id_pedido)
        except ValueError:
            print("== Esse campo aceita apenas números inteiros. ==")
            continue

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT status, cliente_id FROM pedidos WHERE id = %s", (id_pedido_int,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(f"== O pedido {id_pedido_int} não foi encontrado. ==")
            cursor.close(); conn.close()
            continue

        status, cliente_id = resultado
        if status != "feito":
            print("== Esse pedido não pode ser pago por estar em andamento, já ter sido pago ou ter sido cancelado. ==")
            cursor.close(); conn.close()
            continue

        estaPago = input("== O pedido foi pago? ==\n== Escolha um número: ==\n 1. Sim;\n 2. Não.\n")

        if estaPago == "1":
            cursor.execute("UPDATE clientes SET pontos = pontos + 1 WHERE id = %s", (cliente_id,))
            cursor.execute("UPDATE pedidos SET status = 'pago' WHERE id = %s", (id_pedido_int,))
            conn.commit()
            print(f"== O pedido {id_pedido_int} está pago e finalizado. ==")
        elif estaPago == "2":
            print("== Receba o valor do pedido com o cliente. ==")
        else:
            fg.invalid(estaPago)

        cursor.close()
        conn.close()