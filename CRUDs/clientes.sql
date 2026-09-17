CREATE TABLE clientes (
    id          INTEGER PRIMARY KEY,
    nome        VARCHAR(60) NOT NULL,
    telefone    VARCHAR(20),
    email       VARCHAR(100),
    cpf         VARCHAR(11) UNIQUE,
    pontos      INTEGER DEFAULT 0
);