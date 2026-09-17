CREATE TABLE pedido_itens(
    id              SERIAL PRIMARY KEY,
    pedido_id       INTEGER NOT NULL REFERENCES pedidos(id),
    cardapio_id     INTEGER NOT NULL REFERENCES cardapio(id),
    quantidade      INTEGER NOT NULL
);