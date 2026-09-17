CREATE TABLE estoque (
    id          INTEGER PRIMARY KEY,
    ingrediente VARCHAR(60) NOT NULL UNIQUE,
    quantidade  INTEGER NOT NULL DEFAULT 0
);