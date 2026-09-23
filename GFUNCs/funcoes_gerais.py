"""
Esse documento concentra funções comuns nos outros documentos do projeto.
"""

# Função linhaIgual() imprime uma string apenas de caracteres '=' do mesmo tamanho de outra string selecionada dentro do programa, 
# o parâmetro é a própria string selecionada:
def linhaIgual(x):
    lin = len(x)
    print("=" * lin)

# Função 'back()' emite texto padrão para informar ao usuário que o programa está retornando ao menu principal:
def back():
    linhaIgual("== Retornando. ==")
    print("== Retornando. ==")
    linhaIgual("== Retornando. ==")

# Função 'invalid()' emite texto padrão em caso de invalidez de input,
# O parâmetro a ser usado é seja qual for a variável de input que o usuário tiver contato
def invalid(x):
    linhaIgual(f"== O comando '{x}' não é válido. ==")
    print(f"== O comando '{x}' não é válido. ==")
    linhaIgual(f"== O comando '{x}' não é válido. ==")

# Função 'positiveOnly()' emite texto padrão quando o usuário tenta atribuir valor negativo a uma chave que só aceita valores positivos:
def positiveOnly():
    linhaIgual("== Essa variável aceita apenas valores positivos ==")
    print("== Essa variável aceita apenas valores positivos ==")
    linhaIgual("== Essa variável aceita apenas valores positivos ==")

# Função 'changedKey()' emite texto padrão quando uma chave é alterada dentro de algum CRUD:
def changedKey():
    linhaIgual("== Chave alterada com sucesso! ==")
    print("== Chave alterada com sucesso! ==")
    linhaIgual("== Chave alterada com sucesso! ==")

# A função end() é utilizada para emitir texto padrão quando algum dos sistemas do projeto é fechado, utiliza como parâmetro o nome do sistema em questão:
def end(x):
    linhaIgual(f"== Encerrando {x}. ==")
    print(f"== Encerrando {x}. ==")
    linhaIgual(f"== Encerrando {x}. ==")
