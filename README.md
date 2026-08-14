# ☕ Coffee Shops Tia Rosa

<p align= "center">
    <img src="logo.tia.rosa.png" alt="Logo Coffee Shops Tia Rosa" width="300">
</p>

Análise e Desenvolvimento de Sistemas - IESB

Projeto que compõe nota na disciplina: **Lógica - Algoritmos e Programação de Computadores**

Professor: Francisco Filho

## 🎯 Objetivo
> Criar um sistema para a cafeteria da tia Rosa que deve incluir:
1. Cardápio com descrição dos pratos;
2. Sistemas CRUD's de estoque de ingredientes e cadastro dos clientes;
3. Sistema de numeração de pedidos para formação de histórico juntamente com os produtos selecionados em cada pedido.
> As funcionalidades do sistema devem ser simples para que os colaboradores consigam se familiarizar rapidamente.
> Precisa ajudar na fidelização dos clientes.

## ☕ Funcionalidades

- ✅ Menu principal
- ✅ Gerenciamento de produtos
- ✅ Cadastro de clientes
- ✅ Controle de estoque
- ✅ Gerenciamento de pedidos


## 🔀 Fluxograma geral do projeto:

                    ┌──────────────┐
                    │    main.py   │
                    └───┬┬┬┬───────┘
                        ││││┌───────────────────────────┐
                        │││└│    tia_rosa_cardapio.py   │
                        │││ └────────┬──────────────────┘
                        │││ ┌────────┴────────┐
                        ││└─│    estoque.py   │──┐
                        ││   ─────────────────┘  │
                        ││  ┌──────────────────┐ │
                        │└──│    clientes.py   │┐│
                        │   └────────┬─────────┘││
                        │   ┌────────┴────────┐ ││
                        └───│    pedidos.py   │─┘┘
                            └─────────────────┘