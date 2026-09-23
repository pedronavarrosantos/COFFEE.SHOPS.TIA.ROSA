import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "GFUNCs"))

import funcoes_gerais as fg
from db_connection_2 import get_connection

def get_stats_connection():
    conn = get_connection()
    return conn.cursor(), conn

def pedidos_por_cliente():
    cursor, conn = get_stats_connection()
    print("\n" + "="*40)
    print("      ANÁLISE DE CLIENTES")
    print("="*40)
    print("1. Ver Top 10 Clientes (Mais pedidos)")
    print("2. Buscar pedidos de um cliente específico")
    print("0. Voltar")
    
    escolha = input("\nEscolha a opção: ")
    
    if escolha == "1":
        # LIMIT 10 resolve o problema de ter centenas de clientes
        query = """
            SELECT c.nome, COUNT(p.id) as total 
            FROM clientes c 
            JOIN pedidos p ON c.id = p.cliente_id 
            GROUP BY c.nome 
            ORDER BY total DESC 
            LIMIT 10
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        print("\n--- TOP 10 CLIENTES ---")
        for nome, total in resultados:
            print(f"Cliente: {nome:20} | Pedidos: {total}")
            
    elif escolha == "2":
        nome_busca = input("Digite o nome ou ID do cliente: ")
        query = """
            SELECT COUNT(p.id) 
            FROM pedidos p 
            JOIN clientes c ON p.cliente_id = c.id 
            WHERE c.nome ILIKE %s OR CAST(c.id AS TEXT) = %s
        """
        cursor.execute(query, (f"%{nome_busca}%", nome_busca))
        total = cursor.fetchone()[0]
        print(f"\n== O cliente encontrado realizou {total if total else 0} pedido(s). ==")

    cursor.close()
    conn.close()

def media_gastos_por_periodo():
    cursor, conn = get_stats_connection()
    print("\n--- Média de Gastos por Período ---")
    
    # A query permanece a mesma, mas vamos tratar a saída para o usuário
    query = """
        SELECT 
            CASE 
                WHEN EXTRACT(HOUR FROM data_pedido) BETWEEN 6 AND 11 THEN 'Manhã'
                WHEN EXTRACT(HOUR FROM data_pedido) BETWEEN 12 AND 17 THEN 'Tarde'
                ELSE 'Noite'
            END as periodo,
            AVG(valor_total) as media
        FROM pedidos
        WHERE status = 'pago'
        GROUP BY periodo
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("== Nenhum pedido pago encontrado para calcular médias. ==")
    else:
        # Criamos um dicionário com todos os períodos para garantir a exibição
        periodos_esperados = {"Manhã": 0, "Tarde": 0, "Noite": 0}
        for periodo, media in resultados:
            periodos_esperados[periodo] = media
            
        for periodo, media in periodos_esperados.items():
            if media == 0:
                print(f"Período: {periodo:10} | Sem dados registrados.")
            else:
                print(f"Período: {periodo:10} | Média: R$ {media:.2f}")
    
    cursor.close()
    conn.close()

def media_geral_gastos():
    cursor, conn = get_stats_connection()
    # Adicionado COALESCE para retornar 0 caso não haja pedidos, evitando erro de 'None'
    query = "SELECT COALESCE(AVG(valor_total), 0) FROM pedidos WHERE status = 'pago'"
    cursor.execute(query)
    resultado = cursor.fetchone()[0]
    
    print(f"\n== Ticket médio: R$ {resultado:.2f} ==")
    
    cursor.close()
    conn.close()

def dias_mais_faturados():
    cursor, conn = get_stats_connection()
    print("\n--- Faturamento por Dia da Semana ---")
    
    # Mapeamento para traduzir os dias do banco (inglês) para português
    traducao_dias = {
        'Sunday': 'Domingo', 'Monday': 'Segunda', 'Tuesday': 'Terça', 
        'Wednesday': 'Quarta', 'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado'
    }
    
    query = """
        SELECT 
            TO_CHAR(data_pedido, 'Day') as dia, 
            SUM(valor_total) as total
        FROM pedidos 
        WHERE status = 'pago'
        GROUP BY dia
        ORDER BY total DESC
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    if not resultados:
        print("== Sem dados de faturamento. ==")
    else:
        for dia_eng, total in resultados:
            dia_pt = traducao_dias.get(dia_eng.strip(), dia_eng.strip())
            print(f"Dia: {dia_pt:12} | Total: R$ {total:.2f}")
        
    cursor.close()
    conn.close()

def media_valor_por_dia():
    cursor, conn = get_stats_connection()
    print("\n" + "="*40)
    print("   TICKET MÉDIO POR DIA DA SEMANA")
    print("="*40)
    
    # Mapeamento para tradução e para garantir a ordem correta (Domingo a Sábado)
    # A chave é o número retornado pelo EXTRACT(DOW FROM ...) do Postgres
    dias_semana = {
        0: 'Domingo', 1: 'Segunda', 2: 'Terça', 
        3: 'Quarta', 4: 'Quinta', 5: 'Sexta', 6: 'Sábado'
    }
    
    # Query: Agrupamos pelo número do dia da semana (DOW) e calculamos a média
    query = """
        SELECT 
            EXTRACT(DOW FROM data_pedido) as dia_num, 
            AVG(valor_total) as media
        FROM pedidos 
        WHERE status = 'pago'
        GROUP BY dia_num
    """
    cursor.execute(query)
    resultados = cursor.fetchall()
    
    # Transformamos o resultado em um dicionário {numero_do_dia: valor_da_media}
    dados_medias = {dia_num: media for dia_num, media in resultados}
    
    # Agora percorremos o nosso dicionário de dias_semana para imprimir na ordem certa
    for num, nome in dias_semana.items():
        media = dados_medias.get(num)
        if media is not None:
            print(f"{nome:12} | Média de gasto: R$ {media:.2f}")
        else:
            print(f"{nome:12} | Sem pedidos registrados.")
            
    cursor.close()
    conn.close()

def menu_estatisticas():
    while True:
        print("\n" + "="*30)
        print("  SISTEMA DE ANÁLISE DE DADOS")
        print("="*30)
        print("1. Análise de Clientes")
        print("2. Média de Gastos por Período")
        print("3. Média Geral de Pedidos")
        print("4. Dias que mais faturam (Total)")
        print("5. Ticket Médio por Dia da Semana")
        print("0. Voltar")
        
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            pedidos_por_cliente()
        elif opcao == "2":
            media_gastos_por_periodo()
        elif opcao == "3":
            media_geral_gastos()
        elif opcao == "4":
            dias_mais_faturados()
        elif opcao == "5":
            media_valor_por_dia()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu_estatisticas()