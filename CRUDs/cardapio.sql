CREATE TABLE cardapio (
    id          INTEGER PRIMARY KEY,
    nome        VARCHAR(60) NOT NULL,
    preco       DECIMAL(10,2) NOT NULL,
    descricao   VARCHAR(200)
);