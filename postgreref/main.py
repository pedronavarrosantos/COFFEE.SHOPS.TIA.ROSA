import clientes_postgre as clp
import estoque_postgre as ep
import pedidos_postgre as pp
import cardapio_postgre as cap
import funcoes_gerais as fg
import teste_dados as stats  # Seu módulo de estatísticas
import ai_agent as ai       # O novo agente de IA

def sistema_principal():
    while True:
        options = input("\n" + "="*45 + "\n"
        "== Bem-vindo ao sistema do Coffee Shops Tia Rosa! ==\n"
        "== O que deseja acessar? ==\n"
        "=============================================\n"
        " 1. Cardápio\n"
        " 2. Clientes\n"
        " 3. Estoque\n"
        " 4. Pedidos\n"
        " 5. Relatórios de Gestão (Análise de Dados)\n"
        " 6. Sair do sistema\n"
        "=============================================\n"
        "Escolha um número: ")

        if options == "1":
            cap.sistema_cardapio()
        elif options == "2":
            clp.sistema_clientes()
        elif options == "3":
            ep.sistema_estoque()
        elif options == "4":
            pp.sistema_pedidos()
        elif options == "5":
            stats.menu_estatisticas()
        elif options == "6":
            fg.end("sistema Cafeteria Tia Rosa")
            break
        else:
            fg.invalid(options)

if __name__ == "__main__":
    sistema_principal()