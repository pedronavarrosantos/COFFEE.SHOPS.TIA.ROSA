CREATE TABLE cardapio_ingredientes (
    id              SERIAL PRIMARY KEY,
    cardapio_id     INTEGER NOT NULL REFERENCES cardapio(id),
    estoque_id      INTEGER NOT NULL REFERENCES estoque(id)
);