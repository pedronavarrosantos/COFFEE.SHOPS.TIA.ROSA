from flask import Flask, render_template, request, redirect, url_for
import cardapio_postgre as cap
import card_postgre_func as cfunc
import est_postgre_func as ef
import clients_postgre_func as cf
import peds_postgre_func as pf
import teste_dados as stats

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    tem_estoque_baixo = ef.verificar_estoque_baixo()
    resumo = stats.obter_resumo_financeiro()
    pedidos_andamento = pf.obter_qtd_andamento()
    
    # Trocamos 'obter_item_mais_critico' por 'obter_lista_alertas'
    itens_alerta = ef.obter_lista_alertas() 
    
    return render_template('index.html', 
                           aviso_estoque=tem_estoque_baixo, 
                           resumo=resumo,
                           pedidos_andamento=pedidos_andamento,
                           itens_alerta=itens_alerta) # Enviamos a lista completa


@app.route('/cardapio')
def cardapio():
    ordenar_por = request.args.get('sort', 'id')
    direcao = request.args.get('dir', 'ASC')

    dados = cfunc.obter_todos_pratos(ordenar_por=ordenar_por, direcao=direcao) 

    return render_template('cardapio.html', pratos=dados, sort=ordenar_por, dir=direcao)

@app.route('/adicionar_prato')
def pagina_adicionar():
    return render_template('adicionar_prato.html')

@app.route('/salvar_prato', methods=['POST'])
def salvar_prato():
    nome = request.form.get('nome')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')

    cfunc.salvar_prato_db(nome, float(preco), descricao)

    return redirect(url_for('cardapio'))

@app.route('/deletar_prato/<int:id>')
def deletar_prato(id):
    cfunc.deletar_prato_db(id)
    return redirect(url_for('cardapio'))

@app.route('/editar_prato/<int:id>')
def pagina_editar(id):
    prato = cfunc.obter_prato_por_id(id)
    return render_template('editar_prato.html', prato=prato)

@app.route('/atualizar_prato', methods=['POST'])
def atualizar_prato():
    prato_id = request.form.get('id')
    nome = request.form.get('nome')
    preco = request.form.get('preco')
    descricao = request.form.get('descricao')

    cfunc.atualizar_prato_db(prato_id, nome, float(preco), descricao)

    return redirect(url_for('cardapio'))

# --- ROTAS DE CLIENTES ---
@app.route('/clientes')
def clientes():
    termo_pesquisa = request.args.get('search')
    idade_pesquisa = request.args.get('idade')

    ordenar_por = request.args.get('sort', 'id')
    direcao = request.args.get('dir', 'ASC')

    dados_clientes = cf.filtrar_clientes(
        termo=termo_pesquisa, 
        idade=idade_pesquisa, 
        ordenar_por=ordenar_por, 
        direcao=direcao
    )
        
    return render_template('clientes.html', clientes=dados_clientes, sort=ordenar_por, dir=direcao)

@app.route('/adicionar_cliente')
def pagina_adicionar_cliente():
    return render_template('adicionar_cliente.html')

@app.route('/salvar_cliente', methods=['POST'])
def salvar_cliente():
    # Pega os dados do formulário
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    cpf = request.form.get('cpf')
    idade = request.form.get('idade')
    
    # Salva no banco
    cf.salvar_cliente_db(nome, telefone, email, cpf, int(idade))
    return redirect(url_for('clientes'))

@app.route('/editar_cliente/<int:id>')
def pagina_editar_cliente(id):
    cliente = cf.obter_cliente_por_id(id)
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/atualizar_cliente', methods=['POST'])
def atualizar_cliente():
    # Pega os dados do formulário
    id_cliente = request.form.get('id')
    nome = request.form.get('nome')
    telefone = request.form.get('telefone')
    email = request.form.get('email')
    cpf = request.form.get('cpf')
    pontos = request.form.get('pontos')
    idade = request.form.get('idade')
    
    # Atualiza no banco
    cf.atualizar_cliente_db(id_cliente, nome, telefone, email, cpf, int(pontos), int(idade))
    return redirect(url_for('clientes'))

@app.route('/deletar_cliente/<int:id>')
def deletar_cliente(id):
    cf.deletar_cliente_db(id)
    return redirect(url_for('clientes'))

# --- ROTAS DE ESTOQUE ---

@app.route('/estoque')
def estoque():
    nivel = request.args.get('nivel')

    ordenar_por = request.args.get('sort', 'ingrediente')
    direcao = request.args.get('dir', 'ASC')

    dados_estoque = ef.filtrar_estoque(nivel=nivel, ordenar_por=ordenar_por, direcao=direcao)
        
    return render_template('estoque.html', estoque=dados_estoque, nivel_ativo=nivel, sort=ordenar_por, dir=direcao)

@app.route('/adicionar_ingrediente')
def pagina_adicionar_ingrediente():
    return render_template('adicionar_ingrediente.html')

@app.route('/salvar_ingrediente', methods=['POST'])
def salvar_ingrediente():
    nome = request.form.get('nome')
    quantidade = request.form.get('quantidade')
    
    ef.salvar_ingrediente_db(nome, int(quantidade))
    return redirect(url_for('estoque'))

@app.route('/editar_estoque/<int:id>')
def pagina_editar_estoque(id):
    item = ef.obter_ingrediente_por_id(id)
    return render_template('editar_estoque.html', item=item)

@app.route('/atualizar_estoque', methods=['POST'])
def atualizar_estoque():
    ing_id = request.form.get('id')
    quantidade = request.form.get('quantidade')
    
    ef.atualizar_estoque_db(ing_id, int(quantidade))
    return redirect(url_for('estoque'))

# --- ROTAS DE PEDIDOS ---

@app.route('/pedidos')
def pedidos():
    ordenar_por = request.args.get('sort', 'id')
    direcao = request.args.get('dir', 'DESC')

    dados_pedidos = pf.obter_todos_pedidos(ordenar_por=ordenar_por, direcao=direcao)

    return render_template('pedidos.html', pedidos=dados_pedidos, sort=ordenar_por, dir=direcao)


@app.route('/novo_pedido')
def pagina_novo_pedido():
    clientes = cf.obter_todos_clientes()
    pratos = cfunc.obter_todos_pratos(apenas_ativos=True)
    return render_template('novo_pedido.html', clientes=clientes, pratos=pratos)

@app.route('/finalizar_pedido', methods=['POST'])
def finalizar_pedido():
    cliente_id = request.form.get('cliente_id')
    pratos_ids = request.form.getlist('prato_id[]')
    quantidades = request.form.getlist('qtd[]')

    itens_pedido_lista = []
    for pid, qtd in zip(pratos_ids, quantidades):
        if qtd and int(qtd) > 0:
            itens_pedido_lista.append((int(pid), int(qtd)))
    
    sucesso, pedido_id, mensagem = pf.processar_pedido_automatico(int(cliente_id), itens_pedido_lista)
    
    if sucesso:
        return redirect(url_for('pedidos'))
    else:
        return f"Erro ao processar pedido: {mensagem} <br><a href='/novo_pedido'>Tentar novamente</a>"

@app.route('/detalhes_pedido/<int:id>')
def detalhes_pedido(id):
    # 1. Busca as informações básicas do pedido (Cliente, Total, etc)
    info = pf.obter_info_geral_pedido(id)
    
    # 2. Busca a lista de pratos que compõem esse pedido
    itens = pf.obter_itens_do_pedido(id)
    
    # 3. Abre a página passando as duas informações
    return render_template('detalhes_pedido.html', pedido=info, itens=itens)

@app.route('/relatorios')
def relatorios():
    # Coletamos todas as estatísticas do banco
    resumo = stats.obter_resumo_financeiro()
    mais_vendidos = stats.obter_produtos_mais_vendidos()
    clientes_top = stats.obter_clientes_fiéis()
    
    return render_template('relatorios.html', 
                           resumo=resumo, 
                           mais_vendidos=mais_vendidos, 
                           clientes_top=clientes_top)

if __name__ == "__main__":
    app.run(debug=True)