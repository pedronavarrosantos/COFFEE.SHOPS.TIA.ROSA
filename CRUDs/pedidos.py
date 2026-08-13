"""
Sistema de pedidos do Coffee Shops Tia Rosa

-> Assim como nos outros documentos, cada pedido será armazenado na forma de dicionários
-> As chaves de cada pedido serão:
1. Número identificador;
2. Cliente (que será exportado do sistema de clientes);
3. Pratos {que será exportado do sistema de cardápio);
4. Números identificadores dos pratos {que será exportado do sistema de cardápio) com multiplicador de quantidade de cada prato;
5. Preço
6. Situação(Em andamento, feito, pago ou cancelado)

-> A chave 'pontos' presente dos dicionários de clientes progride em valor aqui no sistema de pedidos.
"""

# Como o sistema de pedido interage com chaves de todos os outros dicionários dos documentos .py do sistema, é necessário abrir todos eles em formato leitura:
# Abertura de arquivo, lista e transformação de conteúdo em dicionário do sistema de cardápio:
cardapio = []

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

# Abertura de arquivo, lista e transformação de conteúdo em dicionário do sistema de clientes:
clientes = []

with open("clientes.txt", "r") as doc1:
    for line in doc1:
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
            "pontos": points
        })

# Abertura de arquivo, lista e transformação de conteúdo em dicionário do sistema de estoque:
estoque = []

with open('estoque.txt', 'r') as doc2:
    for line in doc2:
        counter, frag, quantidade_atual = line.split(";")
        counterint = int(counter)
        quantidade_atual = int(quantidade_atual)

        estoque.append({
            "id": counterint,
            "ingrediente": frag,
            "quantidade": quantidade_atual
        })
# Função 'savedoc_estoque()' salva o estoque atualizado em 'estoque.txt':
def savedoc_estoque():
    with open("estoque.txt", "w") as doc:
        for item in estoque:
            doc.write(f"{item['id']};{item['ingrediente']};{item['quantidade']}\n")
# Abertura de arquivo, lista e transformação de conteúdo em dicionário do sistema de pedidos:
pedidos = []

try:
    with open("pedidos.txt", "r") as doc3:
        for line in doc3:
            linha = line.strip()
            if linha == "":
                continue
            rId, rCliente, rPratos, rIdPratos, rPreco, rSituacao = linha.split(";")
 
            pedidos.append({
                "id": int(rId),
                "cliente": int(rCliente),
                "pratos": rPratos.split(","),
                "id_pratos": rIdPratos.split(","),
                "preço": float(rPreco),
                "situação": rSituacao
            })
except FileNotFoundError:
    with open("pedidos.txt", "w") as doc:
        pass
# Função 'savedoc_pedidos()' salva a lista 'pedidos' em 'pedidos.txt':
def savedoc_pedidos():
    with open("pedidos.txt", "w") as doc:
        for pedido in pedidos:
            doc.write(
                f"{pedido['id']};"
                f"{pedido['cliente']};"
                f"{','.join(pedido['pratos'])};"
                f"{','.join(pedido['id_pratos'])};"
                f"{pedido['preço']};"
                f"{pedido['situação']}\n"
            )
# Função linhaIgual() imprime uma string apenas de caracteres '=' do mesmo tamanho de outra string selecionada dentro do programa, 
# o parâmetro é a própria string selecionada:
def linhaIgual(x):
    print("=" * len(x))
# Função 'invalid()' emite texto padrão em caso de invalidez de input, recebe como parâmetro a variável 'escolha', ou 'loc' ou 'options':
def invalid(y):
    linhaIgual(f"== O comando '{y}' não é válido. ==")
    print(f"== O comando '{y}' não é válido. ==")
    linhaIgual(f"== O comando '{y}' não é válido. ==")
# Função 'back()' emite texto padrão para informar ao usuário que o programa está retornando ao menu principal:
def back():
    print("=================")
    print("== Retornando. ==")
    print("=================\n")
# Função 'adicionar()' serve para adicionar pratos verificando disponibilidade de estoque.
def adicionar():
    # A variável abaixo servirá para o caso do usuário inserir um nome ou id de usuário inválido:
    cliente_encontrado = None
 
    while True:
        cliente_input = input("Digite o nome do cliente ou o seu número identificador:\n== Ou digite '0' para retornar. ==\n")
        if cliente_input == "0":
            back()
            break
 
        for cliente in clientes:
            if cliente_input == cliente["clienteNom"] or cliente_input == str(cliente["clienteID"]):
                # Se o valor inserido pelo usuário corresponder a algum valor presente nas chaves "clienteNom" ou "clienteID" dentro de 'cliente,txt'
                # A variável 'cliente_encontrado' assume o valor da chave encontrada.
                cliente_encontrado = cliente
                print(f"Cliente número {cliente['clienteID']}, nome: {cliente['clienteNom']}.\n")
                break
        # Caso o usuário tenha inserido valor inexistente em 'cliente_input', o valor de 'cliente_encontrado' permanece 'None'
        # e o if abaixo é executado:
        if cliente_encontrado is None:
            linhaIgual("== Cliente não encontrado. ==")
            print("== Cliente não encontrado. ==")
            linhaIgual("== Cliente não encontrado. ==")
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
    id_pratos_pedido = []   # ex: "3x2" -> prato de id 3, quantidade 2
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
        for prato in cardapio:
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
            for item in estoque:
                if item["ingrediente"] == frag:
                    item_estoque = item
                    break
 
            disponivel = item_estoque["quantidade"] if item_estoque else 0
            ja_reservado = reservas.get(frag, 0)
            necessario = quantidade + ja_reservado
 
            if necessario > disponivel:
                faltando.append((frag, max(disponivel - ja_reservado, 0)))
 
        if faltando:
            linhaIgual("== Estoque insuficiente para este prato. ==")
            print("== Estoque insuficiente para este prato. ==")
            for frag, sobra in faltando:
                print(f"   - Falta '{frag}': disponível apenas {sobra} unidade(s).")
            linhaIgual("== Estoque insuficiente para este prato. ==")
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
        for item in estoque:
            if item["ingrediente"] == frag:
                item["quantidade"] = item["quantidade"] - qtd_usada
 
    savedoc_estoque()  # grava o novo estoque em 'estoque.txt'
 
    # O id do novo pedido continua a numeração dos pedidos já existentes (ou começa em 100):
    if len(pedidos) == 0:
        id_pedido = 100
    else:
        id_pedido = pedidos[-1]["id"] + 1
 
    pedidos.append({
        "id": id_pedido,
        "cliente": cliente_encontrado["clienteID"],
        "pratos": pratos_pedido,
        "id_pratos": id_pratos_pedido,
        "preço": preco_total,
        "situação": "em andamento"
    })
 
    savedoc_pedidos()  # grava o novo pedido em 'pedidos.txt'
 
    linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
    print(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
    linhaIgual(f"== Pedido nº {id_pedido} criado com sucesso! Total: R$ {preco_total:.2f} ==")
#Bloco de código em que ocorre toda a manipulação de pedidos:
while True:
    options = input("== Bem-vindo ao sistema de pedidos do Coffee Shops Tia Rosa! ==\n"
    "== Escolha um número: ==\n"
    " 1. Criar novo pedido;\n"
    " 2. Verificar situação de pedido;\n"
    " 3. Modificar pedido;\n"
    " 4. Entregar pedido;\n"
    " 5. Cancelar pedido;\n"
    " 6. Fechar pedido;\n"
    " 7. Sair do sistema.\n"
    "===============================================================\n")

    if options == "1":
        adicionar()
    elif options == "2":
        pass
    elif options == "3":
        pass
    elif options == "4":
        while True:
            localizar_pedido = input("== Qual pedido será entregue? ==\n == Caso queira retornar ao menu principal digite '0'. ==\n")
 
            if localizar_pedido == "0":
                back()
                break
 
            try:
                id_pedido_busca = int(localizar_pedido)
            except ValueError:
                print("Esse campo aceita apenas números inteiros.")
                continue
 
            found = False
            for pedido in pedidos:
                if id_pedido_busca == pedido["id"]:
                    found = True
                    pedido.update({
                        "situação": "feito"
                    })
                    savedoc_pedidos()
                    print(f"== Pedido nº {id_pedido_busca} marcado como 'feito'. ==")
                    break
            if not found:
                print("== Pedido não encontrado. ==")
    elif options == "5":
        pass
    elif options == "6":
        pass
    elif options == "7":
        print("================================================")
        print("== Encerrando sistema de cadastro de pedidos. ==")
        print("================================================")
        break
    else:
        invalid(options)


