from google import genai
import json
import random
from db_connection_2 import get_connection
import peds_postgre_func as pfun

# --- CONFIGURAÇÃO ---
# Use a sua chave aqui
API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# Modelo que funcionou para você
MODEL_NAME = "gemini-3.5-flash-lite"

# --- CONTEXTO DE MORALTOWN ---
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
    cursor.execute("SELECT id, nome FROM clientes WHERE ativo = TRUE")
    clientes = cursor.fetchall()
    cursor.close()
    conn.close()
    return cardapio, clientes

def definir_persona_demografica():
    sorteio = random.randint(1, 100)
    if sorteio <= 45:
        return "um Idoso da região (prefere tradição, café clássico e calma)"
    elif sorteio <= 65:
        return "um Estudante/Adolescente (prefere itens doces e snacks)"
    elif sorteio <= 75:
        return "uma Criança acompanhada (prefere chocolate e doces)"
    else:
        return "um Adulto trabalhador do comércio local (busca rapidez e energia)"

def simular_clientes(quantidade=1):
    cardapio, clientes = buscar_dados_loja()
    
    if not cardapio or not clientes:
        print("❌ Erro: Cadastre pratos e clientes antes de simular!")
        return

    for i in range(quantidade):
        cliente = random.choice(clientes)
        persona = definir_persona_demografica()

        prompt = f"""
        {LORE_MORALTOWN}
        Você agora é {persona}. Seu nome é {cliente[1]} (ID: {cliente[0]}).
        Cardápio disponível: {cardapio}
        
        Com base na sua persona e no contexto de MoralTown, escolha de 1 a 3 pratos para pedir.
        Responda APENAS em formato JSON:
        {{"cliente_id": {cliente[0]}, "pedido": [[id_do_prato, quantidade], [id_do_prato, quantidade]]}}
        """
        
        try:
            # AQUI ESTÁ A CORREÇÃO CRUCIAL: 
            # Usando argumentos nomeados (model= e contents=) para evitar o erro de 'positional argument'
            response = client.models.generate_content(
                model=MODEL_NAME, 
                contents=prompt
            )
            
            texto_json = response.text.replace('```json', '').replace('```', '').strip()
            dados = json.loads(texto_json)
            
            print(f"🤖 {cliente[1]} entrou na loja como {persona}...")
            
            # Chamada da função no peds_postgre_func.py (espera 3 retornos: sucesso, id, msg)
            sucesso, pedido_id, msg = pfun.processar_pedido_automatico(dados['cliente_id'], dados['pedido'])
            
            if sucesso:
                print(f"✅ {msg}")
                # Fecha o ciclo automaticamente
                pfun.marcar_como_entregue_auto(pedido_id)
                pfun.marcar_como_pago_auto(pedido_id)
                print(f"💰 Pedido {pedido_id} entregue e pago com sucesso!")
            else:
                print(f"❌ {cliente[1]} desistiu do pedido: {msg}")
                
        except Exception as e:
            print(f"⚠️ Erro na simulação do cliente {i+1}: {e}")

if __name__ == "__main__":
    simular_clientes(2)