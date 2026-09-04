"""
Esse documento concentra funções comuns nos outros documentos do projeto.
"""

# Função 'back()' emite texto padrão para informar ao usuário que o programa está retornando ao menu principal:
def back():
    print("=================")
    print("== Retornando. ==")
    print("=================\n")

# Função 'invalid()' emite texto padrão em caso de invalidez de input,
# O parâmetro a ser usado é seja qual for a variável de input que o usuário tiver contato
def invalid(x):
    print("=================================")
    print(f"== O comando '{x}' não é válido. ==")
    print("=================================")

# Função 'positiveOnly()' emite texto padrão quando o usuário tenta atribuir valor negativo a uma chave que só aceita valores positivos:
def positiveOnly():
    print("===================================================")
    print("== Essa variável aceita apenas valores positivos ==")
    print("===================================================\n")
# Função linhaIgual() imprime uma string apenas de caracteres '=' do mesmo tamanho de outra string selecionada dentro do programa, 
# o parâmetro é a própria string selecionada:
def linhaIgual(x):
    lin = len(x)
    print("=" * lin)