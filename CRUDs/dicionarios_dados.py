"""
Esse documento serve para acessar os dados dos arquivos txt do projeto e transformar cada um em dicionários.
"""

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

# Lista que guarda os clientes em memória:
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

# Lista que guarda os ingredientes do cardápio em memória:
ingredientes = []

# Função que trata dados do dicionários de cardápios, identifica ingredientes e os compila em uma lista de dicionários:
def carregarEstoque():
    quantidades_salvas = {}
    try:
        with open("estoque.txt", "r") as doc:
            for line in doc:
                _id, _ingrediente, _quantidade = line.split(";")
                quantidades_salvas[_ingrediente] = int(_quantidade)
    except FileNotFoundError:
        # Primeira execução: ainda não existe 'estoque.txt', então não há quantidades pra recuperar.
        pass
    # A lista "ingredientes = []" recebe os dicionários de cada ingrediente dos pratos:
    
    # Variável 'counter' serve para aumentar gradativamente a enumeração dos ingredientes. É o insumo da chave "id"
    counter = 0

    # O for abaixo inicia a separação da chave "ingredientes" em fragmentos:
    for prato in cardapio:
        fragmentos = prato["ingredientes"].split(",")

        # Remove espaços em branco de todos os fragmentos:
        fragmentos = [frag.strip() for frag in fragmentos]

        # Remove as aspas simples apenas do primeiro e do último fragmento da linha:
        fragmentos[0] = fragmentos[0].strip("'")
        fragmentos[-1] = fragmentos[-1].strip("'")

        # Com os fragmentos tratados, o append à lista "ingredientes = []" é feito no for abaixo:
        for frag in fragmentos:
            if frag not in [item["ingrediente"] for item in ingredientes]:
                quantidade_atual = quantidades_salvas.get(frag, 0)

                ingredientes.append({
                    "id": counter,
                    "ingrediente": frag,
                    "quantidade": quantidade_atual
                })
                counter += 1

# Abertura de arquivo, lista e transformação de conteúdo em dicionário do sistema de pedidos:
pedidos = []

def carregarPedidos():
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

# Abertura de arquivo, lista e transformação de conteúdo em dicionário do sistema de estoque:
estoque = []

def estruturarEstoque():
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