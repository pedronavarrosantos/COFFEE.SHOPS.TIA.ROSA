"""
Esse documento concentra as funções de manupulação do arquivo CRUD pedidos.py
"""
import funcoes_gerais
import dicionarios_dados

dicionarios_dados.carregarcardapio()
dicionarios_dados.carregarclientes()
dicionarios_dados.carregarEstoque()
dicionarios_dados.carregarPedidos()
dicionarios_dados.estruturarEstoque()

# Função 'savedoc_estoque()' salva o estoque atualizado em 'estoque.txt':
def savedoc_estoque():
    with open("estoque.txt", "w") as doc:
        for item in dicionarios_dados.estoque:
            doc.write(f"{item['id']};{item['ingrediente']};{item['quantidade']}\n")

# Função 'savedoc_clientes()' salva a lista 'clientes' em 'clientes.txt' (mesmo formato usado em clientes.py):
def savedoc_clientes():
    with open("clientes.txt", "w") as doc:
        for cliente in dicionarios_dados.clientes:
            doc.write(
                f"{cliente['clienteNom']};"
                f"{cliente['clienteID']};"
                f"{cliente['telefone']};"
                f"{cliente['e-mail']};"
                f"{cliente['cpf']};"
                f"{cliente['pontos']}\n"
            )

# Função 'savedoc_pedidos()' salva a lista 'pedidos' em 'pedidos.txt':
def savedoc_pedidos():
    with open("pedidos.txt", "w") as doc:
        for pedido in dicionarios_dados.pedidos:
            doc.write(
                f"{pedido['id']};"
                f"{pedido['cliente']};"
                f"{','.join(pedido['pratos'])};"
                f"{','.join(pedido['id_pratos'])};"
                f"{pedido['preço']};"
                f"{pedido['situação']}\n"
            )

# Função 'adicionar()' serve para adicionar pratos verificando disponibilidade de estoque.
def adicionar():
    # A variável abaixo servirá para o caso do usuário inserir um nome ou id de usuário inválido:
    cliente_encontrado = None
    # Inicialmente é necessário localizar o cliente para montar o pedido, o while abaixo faz isso:
    while True:
        cliente_input = input("Digite o nome do cliente ou o seu número identificador:\n== Ou digite '0' para retornar. ==\n")
        if cliente_input == "0":
            funcoes_gerais.back()
            break
 
        for cliente in dicionarios_dados.clientes:
            if cliente_input == cliente["clienteNom"] or cliente_input == str(cliente["clienteID"]):
                # Se o valor inserido pelo usuário corresponder a algum valor presente nas chaves "clienteNom" ou "clienteID" dentro de 'cliente,txt'
                # A variável 'cliente_encontrado' assume o valor da chave encontrada.
                cliente_encontrado = cliente
                print(f"Cliente número {cliente['clienteID']}, nome: {cliente['clienteNom']}.\n")
                break
        # Caso o usuário tenha inserido valor inexistente em 'cliente_input', o valor de 'cliente_encontrado' permanece 'None'
        # e o if abaixo é executado:
        if cliente_encontrado is None:
            funcoes_gerais.linhaIgual("== Cliente não encontrado. ==")
            print("== Cliente não encontrado. ==")
            funcoes_gerais.linhaIgual("== Cliente não encontrado. ==")
            continue
        else:
            break
 
    # Se o cliente não foi encontrado (usuário digitou '0' para sair), não continua o pedido.
    # Dentro de uma função, "desistir e não continuar" é 'return' (sai da função), não 'continue'
    # (que só existe dentro de um loop) — não há mais um 'while' do menu principal aqui dentro.
    if cliente_encontrado is None:
        return
 
    # ===== ETAPA 2: montar o pedido, prato por prato =====
    # Listas/variáveis que vão virar as chaves do dicionário do pedido:
    pratos_pedido = []      # nomes dos pratos adicionados
    id_pratos_pedido = []   # 'id' vezes quantidade
    preco_total = 0
 
    # 'reservas' guarda, ingrediente por ingrediente, quanto já foi comprometido dentro
    # deste mesmo pedido. Isso evita que dois pratos diferentes do mesmo pedido "furem"
    # o estoque um do outro antes de o pedido ser fechado.
    reservas = {}
 
    while True:
        produto = input("Digite o nome do prato ou o seu número identificador:\n== Ou digite '0' para finalizar o pedido. ==\n")
        if produto == "0":
            break
 
        prato_encontrado = None
        for prato in dicionarios_dados.cardapio:
            if produto == prato["nome"] or produto == str(prato["identificação"]):
                prato_encontrado = prato
                break
 
        if prato_encontrado is None:
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
 
        # Fragmenta a chave "ingredientes" do prato, do mesmo jeito que estoque.py faz:
        fragmentos = prato_encontrado["ingredientes"].split(",")
        fragmentos = [frag.strip().strip("'") for frag in fragmentos]
 
        # Verifica, para cada ingrediente do prato, se o estoque aguenta a quantidade pedida
        # (somando o que já está reservado por outros pratos deste mesmo pedido):
        faltando = []
        for frag in fragmentos:
            item_estoque = None
            for item in dicionarios_dados.estoque:
                if item["ingrediente"] == frag:
                    item_estoque = item
                    break
 
            disponivel = item_estoque["quantidade"] if item_estoque else 0
            ja_reservado = reservas.get(frag, 0)
            necessario = quantidade + ja_reservado
 
            if necessario > disponivel:
                faltando.append((frag, max(disponivel - ja_reservado, 0)))
 
        if faltando:
            funcoes_gerais.linhaIgual("== Estoque insuficiente para este prato. ==")
            print("== Estoque insuficiente para este prato. ==")
            for frag, sobra in faltando:
                print(f"   - Falta '{frag}': disponível apenas {sobra} unidade(s).")
            funcoes_gerais.linhaIgual("== Estoque insuficiente para este prato. ==")
            continue
 
        # Passou na verificação: reserva os ingredientes (ainda não grava no estoque.txt,
        # isso só acontece quando o pedido inteiro for fechado, mais abaixo):
        for frag in fragmentos:
            reservas[frag] = reservas.get(frag, 0) + quantidade
 
        pratos_pedido.append(prato_encontrado["nome"])
        id_pratos_pedido.append(f"{prato_encontrado['identificação']}x{quantidade}")
        preco_total += prato_encontrado["preço"] * quantidade
 
        print(f"== '{prato_encontrado['nome']}' (x{quantidade}) adicionado ao pedido. ==")
 
    # ===== ETAPA 3: fechar o pedido =====
    if not pratos_pedido:
        print("== Pedido cancelado: nenhum prato foi adicionado. ==")
        return
 
    # Agora sim desconta de verdade os ingredientes reservados do estoque em memória:
    for frag, qtd_usada in reservas.items():
        for item in dicionarios_dados.estoque:
            if item["ingrediente"] == frag:
                item["quantidade"] = item["quantidade"] - qtd_usada
 
    savedoc_estoque()  # grava o novo estoque em 'estoque.txt'
 
    # O id do novo pedido continua a numeração dos pedidos já existentes (ou começa em 100):
    if len(dicionarios_dados.pedidos) == 0:
        id_pedido = 100
    else:
        id_pedido = dicionarios_dados.pedidos[-1]["id"] + 1
    
    if cliente_encontrado["pontos"] < 5:
        dicionarios_dados.pedidos.append({
            "id": id_pedido,
            "cliente": cliente_encontrado["clienteID"],
            "pratos": pratos_pedido,
            "id_pratos": id_pratos_pedido,
            "preço": preco_total,
            "situação": "em andamento"
        })
        savedoc_pedidos()
    
        funcoes_gerais.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
        print(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
        funcoes_gerais.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
    else:
        preco_descontado = preco_total * 0.85
        dicionarios_dados.pedidos.append({
            "id": id_pedido,
            "cliente": cliente_encontrado["clienteID"],
            "pratos": pratos_pedido,
            "id_pratos": id_pratos_pedido,
            "preço": preco_descontado,
            "situação": "em andamento"
        })
        savedoc_pedidos()

        cliente_encontrado.update({
            "pontos": cliente_encontrado["pontos"] - 5
        })
        savedoc_clientes()

        valor_desc = preco_total - preco_descontado
    
        funcoes_gerais.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
        print(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_descontado:.2f} ==")
        funcoes_gerais.linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
        print(f"== Esse pedido teve o desconto de fidelidade. ==\n== Valor sem desconto R$ {preco_total:.2f}, valor com desconto R$ {preco_descontado:.2f} ==\n"
        f"Valor do desconto: R$ {valor_desc:.2f}.")

# A 'função buscar_prato()' serve para buscar um prato no cardápio por nome ou identificação:
def buscar_prato(produto_input):
    for prato in dicionarios_dados.cardapio:
        if produto_input == prato["nome"] or produto_input == str(prato["identificação"]):
            return prato
    else:
        return None
# A função 'fragmentar_ingredientes()' fragmenta a chave "ingredientes" de um prato:
def fragmentar_ingredientes(prato):
    fragmentos = prato["ingredientes"].split(",")
    return [frag.strip().strip("'") for frag in fragmentos]
# A função 'verificar_estoque()' verifica se o estoque atual aguenta tirar 'quantidade' unidades de cada ingrediente da lista.
# Retorna uma lista de (ingrediente, disponível) para os que faltam; lista vazia = estoque ok.
def verificar_estoque(fragmentos, quantidade):
    faltando = []
    for frag in fragmentos:
        item_estoque = None
        for item in estoque:
            if item["ingrediente"] == frag:
                item_estoque = item
                break
        disponivel = item_estoque["quantidade"] if item_estoque else 0
        if quantidade > disponivel:
            faltando.append((frag, disponivel))
    return faltando 
# A função 'ajustar_estoque()' desconta 'quantidade' unidades de cada ingrediente da lista de fragmentos (usa número negativo para devolver):
def ajustar_estoque(fragmentos, quantidade):
    for frag in fragmentos:
        for item in estoque:
            if item["ingrediente"] == frag:
                item["quantidade"] -= quantidade
# A função 'buscar_prato_por_id()' localiza, no cardápio, o prato de identificação 'id_prato' (usado pra reler pratos já salvos em 'id_pratos'):
def buscar_prato_por_id(id_prato):
    for prato in dicionarios_dados.cardapio:
        if prato["identificação"] == id_prato:
            return prato
    return None
# Mostra os pratos de um pedido numerados, pra o usuário escolher a linha em remoção/alteração:
def listar_pratos_do_pedido(pedido):
    for i, idp in enumerate(pedido["id_pratos"]):
        print(f"  {i + 1}. {pedido['pratos'][i]} ({idp})")
# Pede ao usuário o número da linha (1, 2, 3...) de um prato dentro do pedido e devolve o índice (0, 1, 2...).
# Devolve None se o usuário cancelar ('0') ou digitar algo inválido.
def escolher_linha_do_pedido(pedido):
    if not pedido["id_pratos"]:
        print("== Este pedido não tem pratos. ==")
        return None
 
    listar_pratos_do_pedido(pedido)
    escolha = input("Digite o número da linha do prato:\n== Ou digite '0' para cancelar. ==\n")
    if escolha == "0":
        return None
 
    try:
        indice = int(escolha) - 1
    except ValueError:
        print("== Digite apenas números inteiros. ==")
        return None
 
    if indice < 0 or indice >= len(pedido["id_pratos"]):
        print("== Número de linha inválido. ==")
        return None
    return indice
# A função 'adicionar_prato_ao_pedido()' insere um novo prato num pedido já existente:
def adicionar_prato_ao_pedido(pedido):
    produto = input("Digite o nome do prato ou o seu número identificador a adicionar:\n== Ou digite '0' para cancelar. ==\n")
    if produto == "0":
        return
 
    prato = buscar_prato(produto)
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
 
    fragmentos = fragmentar_ingredientes(prato)
    faltando = verificar_estoque(fragmentos, quantidade)
    if faltando:
        funcoes_gerais.linhaIgual("== Estoque insuficiente para este prato. ==")
        print("== Estoque insuficiente para este prato. ==")
        for frag, disponivel in faltando:
            print(f"   - Falta '{frag}': disponível apenas {disponivel} unidade(s).")
        funcoes_gerais.linhaIgual("== Estoque insuficiente para este prato. ==")
        return
 
    ajustar_estoque(fragmentos, quantidade)
    savedoc_estoque()
 
    pedido["pratos"].append(prato["nome"])
    pedido["id_pratos"].append(f"{prato['identificação']}x{quantidade}")
    pedido["preço"] += prato["preço"] * quantidade
    savedoc_pedidos()
 
    print(f"== '{prato['nome']}' (x{quantidade}) adicionado ao pedido nº {pedido['id']}. ==")
# Função 'remover_prato_do_pedido()' tira um prato de um pedido já existente e devolve os ingredientes ao estoque:
def remover_prato_do_pedido(pedido):
    indice = escolher_linha_do_pedido(pedido)
    if indice is None:
        return
 
    id_prato_texto, quantidade_texto = pedido["id_pratos"][indice].split("x")
    id_prato = int(id_prato_texto)
    quantidade = int(quantidade_texto)
 
    prato = buscar_prato_por_id(id_prato)
    if prato is not None:
        fragmentos = fragmentar_ingredientes(prato)
        ajustar_estoque(fragmentos, -quantidade)  # número negativo -> devolve ao estoque
        savedoc_estoque()
        pedido["preço"] -= prato["preço"] * quantidade
 
    nome_removido = pedido["pratos"].pop(indice)
    pedido["id_pratos"].pop(indice)
    savedoc_pedidos()
 
    print(f"== '{nome_removido}' removido do pedido nº {pedido['id']}. ==")
# A função 'alterar_quantidade_no_pedido()' troca a quantidade de um prato que já está no pedido:
def alterar_quantidade_no_pedido(pedido):
    indice = escolher_linha_do_pedido(pedido)
    if indice is None:
        return
 
    id_prato_texto, quantidade_texto = pedido["id_pratos"][indice].split("x")
    id_prato = int(id_prato_texto)
    quantidade_antiga = int(quantidade_texto)
 
    prato = buscar_prato_por_id(id_prato)
    if prato is None:
        print("== Prato não encontrado no cardápio. ==")
        return
 
    try:
        quantidade_nova = int(input("Digite a nova quantidade:\n"))
    except ValueError:
        print("== Digite apenas números inteiros. ==")
        return
    if quantidade_nova <= 0:
        print("== Esse campo aceita apenas valores inteiros positivos. Use a opção de remover se quiser tirar o prato do pedido. ==")
        return
 
    diferenca = quantidade_nova - quantidade_antiga  # positivo = precisa de mais estoque; negativo = devolve estoque
    fragmentos = fragmentar_ingredientes(prato)
 
    if diferenca > 0:
        faltando = verificar_estoque(fragmentos, diferenca)
        if faltando:
            funcoes_gerais.linhaIgual("== Estoque insuficiente para aumentar a quantidade. ==")
            print("== Estoque insuficiente para aumentar a quantidade. ==")
            for frag, disponivel in faltando:
                print(f"   - Falta '{frag}': disponível apenas {disponivel} unidade(s) a mais.")
            funcoes_gerais.linhaIgual("== Estoque insuficiente para aumentar a quantidade. ==")
            return
 
    ajustar_estoque(fragmentos, diferenca)
    savedoc_estoque()
 
    pedido["id_pratos"][indice] = f"{id_prato}x{quantidade_nova}"
    pedido["preço"] += prato["preço"] * diferenca
    savedoc_pedidos()
 
    print(f"== Quantidade de '{prato['nome']}' alterada de {quantidade_antiga} para {quantidade_nova}. ==")
# A função 'modificar_pedido()' concentra a lógica do item 3 do menu: localizar o pedido e,
# em submenu, adicionar prato, remover prato ou alterar a quantidade de um prato.
def modificar_pedido():
    pedido_encontrado = None
 
    while True:
        localizar = input("Qual o número do pedido que deseja modificar?\n== Ou digite '0' para retornar. ==\n")
        if localizar == "0":
            funcoes_gerais.back()
            return
 
        try:
            id_busca = int(localizar)
        except ValueError:
            print("Esse campo aceita apenas números inteiros.")
            continue
 
        for pedido in dicionarios_dados.pedidos:
            if pedido["id"] == id_busca:
                pedido_encontrado = pedido
                break
 
        if pedido_encontrado is None:
            print("== Pedido não encontrado. ==")
            continue
 
        if pedido_encontrado["situação"] != "em andamento":
            print(f"== Este pedido está '{pedido_encontrado['situação']}' e não pode mais ser modificado. ==")
            pedido_encontrado = None
            continue
 
        break
 
    while True:
        print(f"\n== Pedido nº {pedido_encontrado['id']} — Total atual: R$ {pedido_encontrado['preço']:.2f} ==")
        listar_pratos_do_pedido(pedido_encontrado)
 
        escolha = input(
            "O que deseja fazer?\n"
            "1. Adicionar prato;\n"
            "2. Remover prato;\n"
            "3. Alterar quantidade de um prato;\n"
            "== Ou digite '0' para retornar ao menu principal. ==\n"
        )
 
        if escolha == "0":
            funcoes_gerais.back()
            break
        elif escolha == "1":
            adicionar_prato_ao_pedido(pedido_encontrado)
        elif escolha == "2":
            remover_prato_do_pedido(pedido_encontrado)
        elif escolha == "3":
            alterar_quantidade_no_pedido(pedido_encontrado)
        else:
            funcoes_gerais.invalid(escolha)
# A função entrega() serve para trocar a o status da chave "situação" de um dicionário específico dentre os elementos da lista 'pedidos =[]',
# troca a "situação" de 'em andamento' para 'feito':
def entrega():
    while True:
            localizar_pedido = input("== Qual pedido será entregue? ==\n == Caso queira retornar ao menu principal digite '0'. ==\n")
 
            if localizar_pedido == "0":
                funcoes_gerais.back()
                break
 
            try:
                id_pedido_busca = int(localizar_pedido)
            except ValueError:
                print("Esse campo aceita apenas números inteiros.")
                continue
 
            found = False
            for pedido in dicionarios_dados.pedidos:
                if id_pedido_busca == pedido["id"]:
                    found = True

                    if pedido["situação"] == "em andamento":
                        pedido.update({
                            "situação": "feito"
                        })
                        savedoc_pedidos()
                        print(f"== Pedido nº {id_pedido_busca} marcado como 'feito'. ==")
                        break
                    else:
                        print("== O pedido não pode ser entregue por não se encontrar em fase de andamento. ==")
            if not found:
                print("== Pedido não encontrado. ==")
# A função cancelar() serve para cancelar um pedido. Só é possível cancelar um pedido se a sua chave "situação" tiver valor 'em andamento':
def cancelar():
    while True:
            id_pedido = input("== Digite o número do pedido que deseja cancelar: ==\n"
                "== Ou digite '0' para retornar. ==\n")

            if id_pedido == "0":
                funcoes_gerais.back()
                break

            try:
                id_pedido_int = int(id_pedido)
            except ValueError:
                print("== Esse campo aceita apenas números inteiros. ==")
                continue

            found = False

            for pedido in dicionarios_dados.pedidos:
                if id_pedido_int == pedido["id"]:
                    found = True

                    if pedido["situação"] != "em andamento":
                        print(f"== O pedido de número {id_pedido_int} "
                            "já superou a fase de andamento e não pode mais ser cancelado. ==")
                        break

                    escolha = input("== Realmente deseja cancelar o pedido? ==\n"
                        "== Escolha um número: ==\n"
                        "1. Sim\n"
                        "2. Não\n")

                    if escolha == "1":
                        pedido.update({
                            "situação": "cancelado"
                        })
                        savedoc_pedidos()

                        print(f"== Pedido {id_pedido_int} cancelado. ==")
                        break
                    elif escolha == "2":
                        funcoes_gerais.back()
                        break
            if not found:
                print(f"== O pedido de número {id_pedido_int} não foi encontrado. ==")
# A função 'verificar()' serve para ver em qual situação se encontra um pedido:
def verificar():
    while True:
        id_pedido = input("== Digite o número do pedido que deseja verificar: ==\n"
                "== Ou digite '0' para retornar. ==\n")
        
        if id_pedido == "0":
                funcoes_gerais.back()
                break

        try:
            id_pedido_int = int(id_pedido)
        except ValueError:
            print("== Esse campo aceita apenas números inteiros. ==")
            continue

        found = False

        for pedido in dicionarios_dados.pedidos:
            if id_pedido_int == pedido["id"]:
                found = True

                print(f"== O pedido está {pedido['situação']}. ==")
                break
        if not found:
            print(f"== O pedido {id_pedido} não existe. ==")
# A função 'fechar()' serve para colocar a situação do pedido em 'feito' e adicionar 1 ponto à chave 'pontos' dos clientes:
def fechar():
    while True:
        id_pedido = input("== Digite o número do pedido que deseja fechar: ==\n"
                "== Ou digite '0' para retornar. ==\n")
        
        if id_pedido == "0":
                funcoes_gerais.back()
                break

        try:
            id_pedido_int = int(id_pedido)
        except ValueError:
            print("== Esse campo aceita apenas números inteiros. ==")
            continue

        found = False

        for pedido in dicionarios_dados.pedidos:
            if id_pedido_int == pedido["id"]:
                found = True

                if pedido["situação"] != "feito":
                    print("== Esse pedido não pode ser pago por estar em andamento, já ter sido pago ou ter sido cancelado. ==")
                else:
                    estaPago = input("== O pedido foi pago? ==\n== Escolha um número: ==\n"
                    " 1. Sim;\n"
                    " 2. Não.\n")

                    if estaPago == "1":
                        for cliente in dicionarios_dados.clientes:
                            if cliente['clienteID'] == pedido['cliente']:
                                cliente.update({
                                    "pontos": cliente['pontos'] + 1
                                })
                                savedoc_clientes()

                                pedido.update({
                                    "situação": "pago"
                                })
                                savedoc_pedidos()

                                print(f"== O pedido {id_pedido} está pago e finalizado. ==")
                    elif estaPago == "2":
                        print("== Receba o valor do pedido com o cliente. ==")
                    else:
                        funcoes_gerais.invalid(estaPago)
        if not found:
            print(f"== O pedido {id_pedido} não foi encontrado. ==")