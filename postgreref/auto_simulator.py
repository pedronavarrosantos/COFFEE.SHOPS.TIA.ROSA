import os
import time
import random
from datetime import datetime
from dotenv import load_dotenv
from google import genai
import json
from db_connection_2 import get_connection
import peds_postgre_func as pfun
import clients_postgre_func as cfun

# --- CONFIGURAÇÕES ---
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3.5-flash-lite"

HORA_ABERTURA = 8
HORA_FECHAMENTO = 22

LORE_MORALTOWN = """
Local: Cafeteria Tia Rosa, em MoralTown (150k habitantes).
Ambiente: Rua de comércio com concorrência.
Entorno: Prédios residenciais e escolas de todos os níveis.
Demografia da Região:
- 45% Idosos (Preferem tradição, café clássico e calma).
- 20% Jovens/Adolescentes (Preferem doces e snacks).
- 10% Crianças (Preferem chocolate e doces).
- 25% Adultos não idosos (Buscam rapidez e energia).
"""

def buscar_dados_loja():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM cardapio WHERE ativo = TRUE")
    cardapio = cursor.fetchall()
    cursor.execute("SELECT id, nome, idade FROM clientes WHERE ativo = TRUE")
    clientes = cursor.fetchall()
    cursor.close(); conn.close()
    return cardapio, clientes

def contar_clientes_totais():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM clientes")
    total = cursor.fetchone()[0]
    cursor.close(); conn.close()
    return total

def definir_persona():
    sorteio = random.randint(1, 100)
    if sorteio <= 45: return "um Idoso da região (prefere tradição, café clássico e calma)"
    elif sorteio <= 65: return "um Estudante/Adolescente (prefere itens doces e snacks)"
    elif sorteio <= 75: return "uma Criança acompanhada (prefere chocolate e doces)"
    else: return "um Adulto trabalhador do comércio local (busca rapidez e energia)"

def definir_persona_por_idade(idade):
    if idade is None:
        return definir_persona()
    if idade <= 12:
        return "uma Criança acompanhada (prefere chocolate e doces)"
    elif idade <= 19:
        return "um Estudante/Adolescente (prefere itens doces e snacks)"
    elif idade >= 60:
        return "um Idoso da região (prefere tradição, café clássico e calma)"
    else:
        return "um Adulto trabalhador do comércio local (busca rapidez e energia)"

def limpar_pedidos_pendentes():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM pedidos WHERE status = 'em andamento'")
        pendentes = cursor.fetchall()
        for (pid,) in pendentes:
            pfun.marcar_como_entregue_auto(pid)
            pfun.marcar_como_pago_auto(pid)
    except: pass
    finally:
        cursor.close(); conn.close()

def processar_cliente_ia():
    """Função que lida com a entrada de UM cliente"""
    cardapio, clientes = buscar_dados_loja()
    total_clientes = contar_clientes_totais()
    
    if not cardapio or not clientes: return

    # 1. Decisão: Novo Cliente ou Cliente Antigo?
    chance_novo = 0.45 if total_clientes < 2500 else 0.05
    
    if random.random() < chance_novo:
        persona = definir_persona()
        print(f"🆕 Novo morador de MoralTown atraído pela cafeteria... ({persona})")
        
        prompt_novo = (
            f"{LORE_MORALTOWN}\n"
            f"Crie um novo cliente {persona}. Invente: Nome, Idade, CPF, Email, Tel. Não repita nomes e alterne bem entre nomes masculinos e femininos\n"
            f"IMPORTANTE: gere um número de celular brasileiro plausível e variado (formato DDXXXXXXXXX, 11 dígitos), "
            f"NUNCA use números de exemplo repetidos como 11987654321 ou sequências óbvias.\n"
            f"Responda APENAS em JSON: {{\"nome\": \"\", \"idade\": 0, \"cpf\": \"\", \"email\": \"\", \"tel\": \"\", \"pedido\": [[id, qtd]]}}\n"
            f"Cardápio: {cardapio}"
        )
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt_novo)
            dados_ia = json.loads(response.text.replace('```json', '').replace('```', '').strip())
            
            sucesso_cad, res_cad = cfun.adicionar_cliente_automatico(
                dados_ia['nome'], dados_ia['tel'], dados_ia['email'], dados_ia['cpf'], dados_ia['idade']
            )
            if sucesso_cad:
                cliente_id = res_cad
                print(f"📝 Cliente {dados_ia['nome']} cadastrado! Base: {total_clientes + 1}/2500")
            else:
                print(f"⚠️ Falha ao cadastrar cliente: {res_cad}")
                return
        except Exception as e:
            print(f"⚠️ Erro ao criar novo cliente: {e}"); return
    else:
        cliente = random.choice(clientes)
        cliente_id, nome_cliente, idade_cliente = cliente[0], cliente[1], cliente[2]
        persona = definir_persona_por_idade(idade_cliente)
        print(f"🤖 {nome_cliente} entrou na loja como {persona}...")
        prompt = f"{LORE_MORALTOWN}\nVocê é {persona}. Nome: {nome_cliente} (ID: {cliente_id}).\nCardápio: {cardapio}\nEscolha 1-3 pratos. JSON: {{\"cliente_id\": {cliente_id}, \"pedido\": [[id, qtd]]}}"
        try:
            response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
            dados_ia = json.loads(response.text.replace('```json', '').replace('```', '').strip())
            cliente_id = dados_ia['cliente_id']
        except Exception as e:
            print(f"⚠️ Erro na IA: {e}"); return

    # 2. Finalização do Pedido (Ciclo Completo)
    try:
        pedido_itens = dados_ia['pedido']
        # Importante: pfun.processar_pedido_automatico agora retorna (sucesso, id_pedido, msg)
        sucesso, p_id, msg = pfun.processar_pedido_automatico(cliente_id, pedido_itens)
        if sucesso:
            print(f"✅ {msg}")
            pfun.marcar_como_entregue_auto(p_id)
            pfun.marcar_como_pago_auto(p_id)
            print(f"💰 Pedido {p_id} entregue e pago com sucesso!")
        else:
            print(f"❌ Erro no pedido: {msg}")
    except Exception as e:
        print(f"⚠️ Erro no fechamento do pedido: {e}")

# ==============================================================================
# LOOP PRINCIPAL - O MOTOR DA SIMULAÇÃO
# ==============================================================================
if __name__ == "__main__":
    print("🚀 Simulador de Sociedade de MoralTown Iniciado...")
    print(f"⏰ Horário de Funcionamento: {HORA_ABERTURA}h às {HORA_FECHAMENTO}h")
    
    while True:
        # A cada ciclo, limpa pedidos travados
        limpar_pedidos_pendentes()
        
        # Verifica se está no horário de funcionamento
        if HORA_ABERTURA <= datetime.now().hour < HORA_FECHAMENTO:
            # 50% de chance de entrar um cliente a cada ciclo
            if random.random() < 0.5:
                processar_cliente_ia()
        else:
            # Se estiver fechado, avisa apenas uma vez por hora
            if datetime.now().minute == 0:
                print(f"🌙 {datetime.now().strftime('%H:%M')} - Cafeteria fechada.")

        # AQUI ESTÁ O SLEEP: Ele controla a velocidade do tempo na simulação
        # 60 segundos = 1 minuto de tempo real. 
        # Se quiser que a loja seja mais movimentada, diminua para 10 ou 20.
        time.sleep(30)