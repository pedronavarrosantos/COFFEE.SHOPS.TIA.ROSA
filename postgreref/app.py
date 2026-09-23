from flask import Flask, render_template, request, redirect, url_for
import cardapio_postgre as cap
import card_postgre_func as cfunc

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cardapio')
def cardapio():
    lista_de_pratos = cfunc.obter_todos_pratos() 
    return render_template('cardapio.html', pratos=lista_de_pratos)

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

@app.route('/clientes')
def clientes():
    return "Você entrou na página de Clientes!"

@app.route('/estoque')
def estoque():
    return "Você entrou na página de Estoque!"

@app.route('/pedidos')
def pedidos():
    return "Você entrou na página de Pedidos!"

@app.route('/relatorios')
def relatorios():
    return "Você entrou na página de Relatórios!"

if __name__ == "__main__":
    app.run(debug=True)